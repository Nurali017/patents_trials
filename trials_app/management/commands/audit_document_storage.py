from django.core.management.base import BaseCommand

from trials_app.models import Document
from trials_app.storage import document_file_exists


class Command(BaseCommand):
    help = 'Audit document rows against primary storage and legacy filesystem fallback.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--application-id',
            action='append',
            type=int,
            dest='application_ids',
            help='Limit the audit to one or more application IDs.',
        )
        parser.add_argument(
            '--missing-only',
            action='store_true',
            help='Print only documents whose files are missing.',
        )

    def handle(self, *args, **options):
        queryset = Document.objects.filter(is_deleted=False).select_related('application').order_by('id')

        application_ids = options.get('application_ids') or []
        if application_ids:
            queryset = queryset.filter(application_id__in=application_ids)

        missing_only = options.get('missing_only', False)

        total = queryset.count()
        missing_count = 0
        existing_count = 0
        affected_application_ids = set()

        self.stdout.write('id\tapplication_id\tdocument_type\texists\tfile_name')

        for document in queryset:
            file_name = document.file.name if document.file else ''
            exists = document_file_exists(document)
            if exists:
                existing_count += 1
            else:
                missing_count += 1
                if document.application_id:
                    affected_application_ids.add(document.application_id)

            if missing_only and exists:
                continue

            self.stdout.write(
                f'{document.id}\t{document.application_id or "-"}\t{document.document_type}\t{exists}\t{file_name}'
            )

        self.stdout.write('')
        self.stdout.write(f'Total documents audited: {total}')
        self.stdout.write(f'Existing files: {existing_count}')
        self.stdout.write(f'Missing files: {missing_count}')

        if affected_application_ids:
            app_ids = ', '.join(str(app_id) for app_id in sorted(affected_application_ids))
            self.stdout.write(self.style.WARNING(f'Applications needing re-upload: {app_ids}'))
