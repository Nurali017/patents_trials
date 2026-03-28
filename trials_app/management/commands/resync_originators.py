"""
resync_originators -- re-sync originators from Patents for SortRecords missing them.
"""
from django.core.management.base import BaseCommand
from trials_app.models import SortRecord, SortOriginator


class Command(BaseCommand):
    help = "Re-sync originators from Patents for SortRecords without originators"

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--limit', type=int, default=0)

    def handle(self, *args, **options):
        empty = SortRecord.objects.filter(is_deleted=False).exclude(
            id__in=SortOriginator.objects.values_list('sort_record_id', flat=True)
        )
        count = empty.count()
        self.stdout.write(f'SortRecords without originators: {count}')

        if options['dry_run']:
            self.stdout.write(self.style.WARNING('DRY RUN'))
            return

        limit = options.get('limit') or count
        synced = 0
        errors = 0
        still_empty = 0

        for sr in empty[:limit].iterator():
            try:
                result = sr.sync_from_patents(sync_originators=True)
                if result:
                    # Check if originators were actually created
                    if SortOriginator.objects.filter(sort_record=sr).exists():
                        synced += 1
                    else:
                        still_empty += 1
                else:
                    errors += 1
            except Exception as e:
                errors += 1

        self.stdout.write(f'Synced with originators: {synced}')
        self.stdout.write(f'Synced but still empty (no Patents originators): {still_empty}')
        self.stdout.write(f'Errors: {errors}')

        final = SortRecord.objects.filter(is_deleted=False).exclude(
            id__in=SortOriginator.objects.values_list('sort_record_id', flat=True)
        ).count()
        self.stdout.write(f'Total still without originators: {final}')
