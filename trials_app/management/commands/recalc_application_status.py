"""
recalc_application_status -- Recalculate Application.status for migrated Gosreestr apps.

Uses Gosreestr-style priority resolution (not _update_overall_status):
  1. approved wins → registered
  2. ongoing (continue/planned/trial_*) → in_progress
  3. trial_plan_created → distributed
  4. all removed/rejected → rejected
  5. all withdrawn (excluded) → unchanged

Scope: only applications with migrated_from_gosreestr: tagged oblast states.

Usage:
  python manage.py recalc_application_status --dry-run
  python manage.py recalc_application_status
"""
from django.core.management.base import BaseCommand

from trials_app.models import Application, ApplicationOblastState

MIGRATED_TAG_PREFIX = 'migrated_from_gosreestr:'

ONGOING_STATUSES = {
    'continue', 'planned', 'trial_created', 'trial_in_progress',
    'trial_completed', 'decision_pending', 'decision_made',
}


def resolve_migrated_status(oblast_statuses):
    """Gosreestr-style priority. Withdrawn excluded (as in Gosreestr)."""
    statuses = {s for s in oblast_statuses if s != 'withdrawn'}

    if not statuses:
        return None  # all withdrawn or empty → don't change

    # Priority 1: approved wins
    if 'approved' in statuses:
        return 'registered'

    # Priority 2: ongoing (does NOT include trial_plan_created)
    if statuses & ONGOING_STATUSES:
        return 'in_progress'

    # trial_plan_created → distributed (separate from ongoing)
    if 'trial_plan_created' in statuses:
        return 'distributed'

    # Priority 3: all removed/rejected
    if statuses <= {'removed', 'rejected'}:
        return 'rejected'

    return None  # don't change


class Command(BaseCommand):
    help = "Recalculate Application.status for migrated Gosreestr apps using Gosreestr priority"

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true',
                            help='Show changes without writing to DB')

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('=== DRY RUN ===\n'))

        # Find migrated applications (have at least one migrated_from_gosreestr: tag)
        migrated_app_ids = (
            ApplicationOblastState.objects
            .filter(
                is_deleted=False,
                decision_justification__startswith=MIGRATED_TAG_PREFIX,
            )
            .values_list('application_id', flat=True)
            .distinct()
        )

        apps = Application.objects.filter(
            id__in=list(migrated_app_ids),
            is_deleted=False,
        )
        self.stdout.write(f'Migrated applications: {apps.count()}')

        # Prefetch oblast states
        transitions = {}  # old_status -> new_status -> count
        unchanged = 0
        updated = 0

        for app in apps.iterator():
            oblast_statuses = list(
                ApplicationOblastState.objects
                .filter(application=app, is_deleted=False)
                .values_list('status', flat=True)
            )

            new_status = resolve_migrated_status(oblast_statuses)

            if new_status is None or new_status == app.status:
                unchanged += 1
                continue

            key = f'{app.status} → {new_status}'
            transitions[key] = transitions.get(key, 0) + 1

            if not dry_run:
                Application.objects.filter(id=app.id).update(status=new_status)

            updated += 1

        self.stdout.write(f'\nTransitions:')
        for key, count in sorted(transitions.items()):
            self.stdout.write(f'  {key}: {count}')

        self.stdout.write(f'\nUpdated: {updated}, Unchanged: {unchanged}')

        if not dry_run:
            # Summary
            from django.db.models import Count
            summary = (
                Application.objects
                .filter(id__in=list(migrated_app_ids), is_deleted=False)
                .values('status')
                .annotate(cnt=Count('id'))
                .order_by('-cnt')
            )
            self.stdout.write('\nFinal distribution:')
            for row in summary:
                self.stdout.write(f'  {row["status"]}: {row["cnt"]}')

        self.stdout.write(self.style.SUCCESS('\nDone.'))
