"""
fix_applicant_field -- clear applicant field that was incorrectly filled
with originator names during Gosreestr migration.

Originator != Applicant. Gosreestr has no applicant data, only originators
(which live on sort level via SortRecord -> SortOriginator -> Originator).

SAFETY: Only clears applicant for applications that were CREATED by the
migration (not enriched). Enriched applications already existed before
migration and may have user-entered applicant data.

Usage:
  python manage.py fix_applicant_field --dry-run
  python manage.py fix_applicant_field
"""
import psycopg2
from django.core.management.base import BaseCommand

from trials_app.models import Application


class Command(BaseCommand):
    help = "Clear applicant field incorrectly filled with originator names"

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('=== DRY RUN ===\n'))

        # Build set of originator names from Gosreestr (the values that
        # migrate_gosreestr incorrectly wrote into applicant)
        gos_originator_names = set()
        try:
            conn = psycopg2.connect(
                dbname='gosreestr', user='gosreestr', password='gosreestr',
                host='localhost', port=5432,
            )
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT name FROM registry_originator")
            for (name,) in cur.fetchall():
                gos_originator_names.add(name.strip())
            cur.close()
            conn.close()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Cannot connect to Gosreestr DB: {e}'))
            self.stdout.write('Falling back to LEGACY- prefix only')

        self.stdout.write(f'Gosreestr originator names loaded: {len(gos_originator_names)}')

        # Only target applications that were CREATED by migration:
        # 1. LEGACY- prefix (always created by migration, never pre-existing)
        # 2. applicant matches a Gosreestr originator name exactly
        #    (migration wrote primary originator name into applicant)
        #
        # Enriched applications are EXCLUDED because:
        # - They already existed before migration
        # - migrate_gosreestr skipped them (enriched += 1, no field changes)
        # - Their applicant may be valid user-entered data

        legacy_apps = Application.objects.filter(
            is_deleted=False,
            application_number__startswith='LEGACY-',
        ).exclude(applicant='')

        if gos_originator_names:
            originator_apps = Application.objects.filter(
                is_deleted=False,
                applicant__in=gos_originator_names,
            )
            # Union: LEGACY- apps + apps whose applicant is a known originator name
            target_ids = set(legacy_apps.values_list('id', flat=True)) | set(
                originator_apps.values_list('id', flat=True)
            )
        else:
            target_ids = set(legacy_apps.values_list('id', flat=True))

        apps = Application.objects.filter(id__in=target_ids, is_deleted=False)
        count = apps.count()

        self.stdout.write(f'Applications to clear: {count}')

        if count == 0:
            self.stdout.write('Nothing to fix.')
            return

        # Show sample
        sample = list(apps[:5])
        for app in sample:
            self.stdout.write(f'  {app.application_number}: applicant="{app.applicant[:60]}"')
        if count > 5:
            self.stdout.write(f'  ... and {count - 5} more')

        # Safety: show how many were EXCLUDED (enriched/pre-existing)
        from trials_app.models import ApplicationOblastState
        all_migrated_ids = set(
            ApplicationOblastState.objects.filter(
                is_deleted=False,
                decision_justification__startswith='migrated_from_gosreestr',
            ).values_list('application_id', flat=True)
        )
        excluded = all_migrated_ids - target_ids
        excluded_with_applicant = Application.objects.filter(
            id__in=excluded, is_deleted=False
        ).exclude(applicant='').count()
        self.stdout.write(
            f'Enriched/pre-existing apps preserved (not cleared): '
            f'{excluded_with_applicant}'
        )

        if not dry_run:
            updated = apps.update(applicant='')
            self.stdout.write(self.style.SUCCESS(
                f'Cleared applicant for {updated} applications'
            ))
        else:
            self.stdout.write(f'Would clear applicant for {count} applications')
