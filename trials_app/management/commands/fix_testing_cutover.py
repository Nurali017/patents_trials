"""
fix_testing_cutover -- Fix testing→planned cutover for 2026 Trials rollout.

Gosreestr 'testing' was mapped to 'planned' during migration, but semantically:
- testing + receipt_date < 2026 → 'continue' (ongoing trials from legacy system)
- testing + receipt_date >= 2026 → 'planned' (new apps to be managed in Trials)

Uses Gosreestr receipt_date as source of truth (not Trials submission_date).

Usage:
  python manage.py fix_testing_cutover --dry-run
  python manage.py fix_testing_cutover
  python manage.py fix_testing_cutover --reverse
"""
import psycopg2
from django.core.management.base import BaseCommand

from trials_app.models import Application, ApplicationOblastState

CUTOVER_YEAR = 2026
MIGRATED_TAG_PREFIX = 'migrated_from_gosreestr:'


class Command(BaseCommand):
    help = "Fix testing→planned cutover: pre-2026 testing → continue"

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true',
                            help='Show what would change without modifying data')
        parser.add_argument('--reverse', action='store_true',
                            help='Reverse: continue → planned for migrated records')

    def handle(self, *args, **options):
        self.dry_run = options['dry_run']

        if self.dry_run:
            self.stdout.write(self.style.WARNING('=== DRY RUN ===\n'))

        gos_years = self._load_gosreestr_years()
        self.stdout.write(f'Loaded {len(gos_years)} Gosreestr receipt years')

        if options['reverse']:
            self._reverse()
        else:
            self._forward(gos_years)

        self.stdout.write(self.style.SUCCESS('\nDone.'))

    def _forward(self, gos_years):
        """planned → continue for migrated testing records with receipt_date < 2026."""
        candidates = ApplicationOblastState.objects.filter(
            status='planned',
            is_deleted=False,
            decision_justification__startswith=MIGRATED_TAG_PREFIX,
        )
        self.stdout.write(f'Candidates (planned + migrated tag): {candidates.count()}')

        to_continue = []
        stay_planned = []
        unknown = []

        for aos in candidates.iterator():
            gos_app_id = self._extract_gos_id(aos.decision_justification)
            if gos_app_id is None:
                unknown.append(aos.id)
                continue

            receipt_year = gos_years.get(gos_app_id)
            if receipt_year is not None and receipt_year < CUTOVER_YEAR:
                to_continue.append(aos.id)
            else:
                stay_planned.append(aos.id)

        self.stdout.write(f'  → continue (receipt_date < {CUTOVER_YEAR}): {len(to_continue)}')
        self.stdout.write(f'  → planned (receipt_date >= {CUTOVER_YEAR}): {len(stay_planned)}')
        if unknown:
            self.stdout.write(self.style.WARNING(f'  → unknown (bad tag): {len(unknown)}'))

        if not to_continue:
            self.stdout.write('Nothing to update.')
            return

        if not self.dry_run:
            updated = ApplicationOblastState.objects.filter(
                id__in=to_continue,
            ).update(status='continue')
            self.stdout.write(f'Updated {updated} ApplicationOblastState → continue')

            self._recalc_application_status(to_continue)
        else:
            self.stdout.write(f'Would update {len(to_continue)} records')

    def _reverse(self):
        """continue → planned for migrated records (undo forward)."""
        tagged_continue = ApplicationOblastState.objects.filter(
            status='continue',
            is_deleted=False,
            decision_justification__startswith=MIGRATED_TAG_PREFIX,
        )
        count = tagged_continue.count()
        self.stdout.write(f'Tagged continue records to revert: {count}')

        if not count:
            self.stdout.write('Nothing to revert.')
            return

        affected_ids = list(tagged_continue.values_list('id', flat=True))

        if not self.dry_run:
            updated = tagged_continue.update(status='planned')
            self.stdout.write(f'Reverted {updated} records → planned')

            self._recalc_application_status(affected_ids)
        else:
            self.stdout.write(f'Would revert {count} records')

    def _recalc_application_status(self, oblast_state_ids):
        """Recalculate Application.status for affected apps."""
        affected_app_ids = (
            ApplicationOblastState.objects
            .filter(id__in=oblast_state_ids)
            .values_list('application_id', flat=True)
            .distinct()
        )
        apps = Application.objects.filter(id__in=list(affected_app_ids))
        self.stdout.write(f'Recalculating status for {apps.count()} applications...')

        for app in apps.iterator():
            app._update_overall_status()

        status_counts = {}
        for app in Application.objects.filter(id__in=list(affected_app_ids)):
            status_counts[app.status] = status_counts.get(app.status, 0) + 1
        self.stdout.write(f'  Application status distribution: {status_counts}')

    def _load_gosreestr_years(self):
        """Load {gos_app_id: receipt_year} from Gosreestr DB."""
        conn = psycopg2.connect(
            dbname='gosreestr', user='gosreestr', password='gosreestr',
            host='localhost', port=5432,
        )
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, EXTRACT(YEAR FROM receipt_date)::int "
                "FROM registry_application"
            )
            result = {row[0]: row[1] for row in cur.fetchall()}
            cur.close()
            return result
        finally:
            conn.close()

    @staticmethod
    def _extract_gos_id(justification):
        """Extract gos_app_id from 'migrated_from_gosreestr:123'."""
        if not justification or not justification.startswith(MIGRATED_TAG_PREFIX):
            return None
        try:
            return int(justification[len(MIGRATED_TAG_PREFIX):])
        except (ValueError, IndexError):
            return None
