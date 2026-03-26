import io
import json
import os
import tempfile
from datetime import date
from unittest.mock import patch
from urllib.parse import urlsplit

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from trials_app.models import (
    Application,
    ApplicationDecisionHistory,
    ClimateZone,
    Culture,
    Document,
    Oblast,
    PlannedDistribution,
    Region,
    SortRecord,
    Trial,
    TrialParticipant,
    TrialType,
)


class ApplicationSubmissionTests(APITestCase):
    def setUp(self):
        self.media_dir = tempfile.TemporaryDirectory()
        self.legacy_media_dir = tempfile.TemporaryDirectory()
        self.override = override_settings(
            MEDIA_ROOT=self.media_dir.name,
            LEGACY_MEDIA_ROOT=self.legacy_media_dir.name,
        )
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.addCleanup(self.media_dir.cleanup)
        self.addCleanup(self.legacy_media_dir.cleanup)

        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='submit-user',
            password='submit-pass',
        )
        self.client.force_authenticate(self.user)

        self.oblast = Oblast.objects.create(name='Akmola', code='AKM')
        self.climate_zone = ClimateZone.objects.create(name='Steppe', code='steppe')
        self.region = Region.objects.create(
            name='Shortandy GSU',
            oblast=self.oblast,
            climate_zone=self.climate_zone,
        )
        self.culture = Culture.objects.create(
            culture_id=720,
            name='Spring Wheat',
            code='WHEAT',
        )
        self.sort_record = SortRecord.objects.create(
            sort_id=5001,
            name='Astana 1',
            culture=self.culture,
            synced_at=timezone.now(),
        )

        self.submit_url = '/api/applications/submit/'
        self.documents_url = '/api/documents/'

    def _build_application_payload(self, application_number='APP-2026-001'):
        return {
            'sort_id': self.sort_record.sort_id,
            'application_number': application_number,
            'submission_date': str(date(2026, 1, 15)),
            'applicant': 'KazNIIZiR',
            'applicant_inn_bin': '123456789012',
            'contact_person_name': 'Test User',
            'contact_person_phone': '+77001234567',
            'contact_person_email': 'test@example.com',
            'maturity_group': 'D03',
            'purpose': 'Production trials',
            'target_oblasts': [self.oblast.id],
            'status': 'submitted',
        }

    def _build_submission(self):
        document_meta = [
            {'document_type': 'application_for_testing', 'title': 'Application', 'is_mandatory': True},
            {'document_type': 'breeding_questionnaire', 'title': 'Questionnaire', 'is_mandatory': True},
            {'document_type': 'variety_description', 'title': 'Description', 'is_mandatory': True},
            {'document_type': 'plant_photo_with_ruler', 'title': 'Photo', 'is_mandatory': True},
        ]
        files = [
            SimpleUploadedFile('application.pdf', b'application', content_type='application/pdf'),
            SimpleUploadedFile('questionnaire.pdf', b'questionnaire', content_type='application/pdf'),
            SimpleUploadedFile('description.pdf', b'description', content_type='application/pdf'),
            SimpleUploadedFile('photo.pdf', b'photo', content_type='application/pdf'),
        ]
        return document_meta, files

    def _create_application(self, application_number='APP-TEST-001'):
        application = Application.objects.create(
            application_number=application_number,
            submission_date=date(2026, 1, 15),
            sort_record=self.sort_record,
            applicant='KazNIIZiR',
            created_by=self.user,
        )
        application.target_oblasts.add(self.oblast)
        return application

    def test_submit_creates_application_and_documents_atomically(self):
        document_meta, files = self._build_submission()

        response = self.client.post(
            self.submit_url,
            data={
                'payload': json.dumps(self._build_application_payload()),
                'document_meta': json.dumps(document_meta),
                'documents': files,
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data['documents_count'], 4)

        application = Application.objects.get(application_number='APP-2026-001')
        self.assertEqual(application.documents.filter(is_deleted=False).count(), 4)
        self.assertEqual(application.get_missing_mandatory_documents(), [])

        documents = list(application.documents.filter(is_deleted=False).order_by('id'))
        self.assertEqual(len(documents), 4)
        for document in documents:
            self.assertTrue(os.path.exists(document.file.path), document.file.path)

    def test_submit_rolls_back_when_storage_save_fails(self):
        document_meta, files = self._build_submission()
        applications_before = Application.objects.count()
        documents_before = Document.objects.count()

        with patch('django.core.files.storage.FileSystemStorage._save', side_effect=PermissionError('no write')):
            response = self.client.post(
                self.submit_url,
                data={
                    'payload': json.dumps(self._build_application_payload('APP-2026-ROLLBACK')),
                    'document_meta': json.dumps(document_meta),
                    'documents': files,
                },
                format='multipart',
        )

        self.assertEqual(response.status_code, 500, response.data)
        self.assertEqual(response.data['code'], 'storage_unavailable')
        self.assertEqual(Application.objects.count(), applications_before)
        self.assertEqual(Document.objects.count(), documents_before)
        self.assertFalse(Application.objects.filter(application_number='APP-2026-ROLLBACK').exists())


class ApplicationEditTests(APITestCase):
    def setUp(self):
        self.media_dir = tempfile.TemporaryDirectory()
        self.legacy_media_dir = tempfile.TemporaryDirectory()
        self.override = override_settings(
            MEDIA_ROOT=self.media_dir.name,
            LEGACY_MEDIA_ROOT=self.legacy_media_dir.name,
        )
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.addCleanup(self.media_dir.cleanup)
        self.addCleanup(self.legacy_media_dir.cleanup)

        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='edit-user',
            password='edit-pass',
        )
        self.client.force_authenticate(self.user)

        self.oblast = Oblast.objects.create(name='Akmola', code='AKM')
        self.second_oblast = Oblast.objects.create(name='Kostanay', code='KST')
        self.climate_zone = ClimateZone.objects.create(name='Steppe', code='steppe')
        self.region = Region.objects.create(
            name='Shortandy GSU',
            oblast=self.oblast,
            climate_zone=self.climate_zone,
        )
        self.second_region = Region.objects.create(
            name='Kostanay GSU',
            oblast=self.second_oblast,
            climate_zone=self.climate_zone,
        )
        self.culture = Culture.objects.create(
            culture_id=720,
            name='Spring Wheat',
            code='WHEAT',
        )
        self.sort_record = SortRecord.objects.create(
            sort_id=5001,
            name='Astana 1',
            culture=self.culture,
            synced_at=timezone.now(),
        )
        self.second_sort_record = SortRecord.objects.create(
            sort_id=5002,
            name='Astana 2',
            culture=self.culture,
            synced_at=timezone.now(),
        )
        self.trial_type = TrialType.objects.create(
            code='competitive',
            name='Competitive',
            name_full='Competitive trial',
        )
        self.documents_url = '/api/documents/'

    def _create_application(self, application_number='APP-EDIT-001', target_oblasts=None):
        application = Application.objects.create(
            application_number=application_number,
            submission_date=date(2026, 1, 15),
            sort_record=self.sort_record,
            applicant='KazNIIZiR',
            applicant_inn_bin='123456789012',
            contact_person_name='Test User',
            contact_person_phone='+77001234567',
            contact_person_email='test@example.com',
            maturity_group='D03',
            purpose='Production trials',
            created_by=self.user,
        )
        application.target_oblasts.set(target_oblasts or [self.oblast])
        return application

    def _build_update_payload(self, application, **overrides):
        payload = {
            'application_number': application.application_number,
            'submission_date': str(application.submission_date),
            'applicant': application.applicant,
            'applicant_inn_bin': application.applicant_inn_bin,
            'contact_person_name': application.contact_person_name,
            'contact_person_phone': application.contact_person_phone,
            'contact_person_email': application.contact_person_email,
            'maturity_group': application.maturity_group,
            'purpose': application.purpose,
            'target_oblasts': list(application.target_oblasts.values_list('id', flat=True)),
        }
        payload.update(overrides)
        return payload

    def test_update_application_without_sort_id_allows_safe_field_changes(self):
        application = self._create_application()
        ApplicationDecisionHistory.objects.create(
            application=application,
            oblast=self.oblast,
            year=2026,
            decision='continue',
            decision_date=date(2026, 10, 1),
            years_tested_total=1,
        )

        response = self.client.put(
            f'/api/applications/{application.id}/',
            data=self._build_update_payload(
                application,
                applicant='Updated Applicant',
                contact_person_name='Updated Contact',
                purpose='Updated purpose',
            ),
            format='json',
        )

        self.assertEqual(response.status_code, 200, response.data)
        application.refresh_from_db()
        self.assertEqual(application.applicant, 'Updated Applicant')
        self.assertEqual(application.contact_person_name, 'Updated Contact')
        self.assertEqual(application.purpose, 'Updated purpose')
        self.assertEqual(application.sort_record_id, self.sort_record.id)

    def test_update_application_blocks_sort_change_when_trial_participant_exists(self):
        application = self._create_application()
        trial = Trial.objects.create(
            region=self.region,
            trial_type=self.trial_type,
            culture=self.culture,
            start_date=date(2026, 5, 1),
            year=2026,
            status='active',
            created_by=self.user,
        )
        TrialParticipant.objects.create(
            trial=trial,
            sort_record=self.sort_record,
            application=application,
            statistical_group=1,
            participant_number=1,
        )

        response = self.client.put(
            f'/api/applications/{application.id}/',
            data=self._build_update_payload(
                application,
                sort_id=self.second_sort_record.sort_id,
            ),
            format='json',
        )

        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn('sort_id', response.data)
        application.refresh_from_db()
        self.assertEqual(application.sort_record_id, self.sort_record.id)

    def test_update_application_blocks_sort_change_when_decision_history_exists(self):
        application = self._create_application()
        ApplicationDecisionHistory.objects.create(
            application=application,
            oblast=self.oblast,
            year=2026,
            decision='approved',
            decision_date=date(2026, 10, 5),
            years_tested_total=1,
        )

        response = self.client.put(
            f'/api/applications/{application.id}/',
            data=self._build_update_payload(
                application,
                sort_id=self.second_sort_record.sort_id,
            ),
            format='json',
        )

        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn('sort_id', response.data)

    def test_update_application_blocks_removing_oblast_with_planned_distribution(self):
        application = self._create_application(target_oblasts=[self.oblast, self.second_oblast])
        PlannedDistribution.objects.create(
            application=application,
            region=self.second_region,
            trial_type=self.trial_type,
            created_by=self.user,
        )

        response = self.client.put(
            f'/api/applications/{application.id}/',
            data=self._build_update_payload(
                application,
                target_oblasts=[self.oblast.id],
            ),
            format='json',
        )

        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn('target_oblasts', response.data)

    def test_update_application_allows_adding_new_oblast(self):
        application = self._create_application()

        response = self.client.put(
            f'/api/applications/{application.id}/',
            data=self._build_update_payload(
                application,
                target_oblasts=[self.oblast.id, self.second_oblast.id],
            ),
            format='json',
        )

        self.assertEqual(response.status_code, 200, response.data)
        application.refresh_from_db()
        self.assertEqual(
            set(application.target_oblasts.values_list('id', flat=True)),
            {self.oblast.id, self.second_oblast.id},
        )
        self.assertTrue(application.oblast_states.filter(oblast=self.second_oblast, is_deleted=False).exists())

    def test_document_update_changes_metadata_and_replaces_file(self):
        application = self._create_application()
        document = Document.objects.create(
            title='Original',
            document_type='application_for_testing',
            application=application,
            uploaded_by=self.user,
            is_mandatory=True,
            file=SimpleUploadedFile('original.pdf', b'original', content_type='application/pdf'),
        )

        response = self.client.patch(
            f'/api/documents/{document.id}/',
            data={
                'title': 'Updated',
                'document_type': 'other',
                'is_mandatory': False,
                'file': SimpleUploadedFile('updated.pdf', b'updated', content_type='application/pdf'),
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, 200, response.data)
        document.refresh_from_db()
        self.assertEqual(document.title, 'Updated')
        self.assertEqual(document.document_type, 'other')
        self.assertFalse(document.is_mandatory)
        self.assertIn('updated', document.file.name)

    def test_document_update_returns_structured_storage_error_when_file_save_fails(self):
        application = self._create_application('APP-EDIT-STORAGE-001')
        document = Document.objects.create(
            title='Original',
            document_type='application_for_testing',
            application=application,
            uploaded_by=self.user,
            is_mandatory=True,
            file=SimpleUploadedFile('original.pdf', b'original', content_type='application/pdf'),
        )

        with patch('django.core.files.storage.FileSystemStorage._save', side_effect=PermissionError('no write')):
            response = self.client.patch(
                f'/api/documents/{document.id}/',
                data={
                    'title': 'Updated',
                    'document_type': 'other',
                    'is_mandatory': False,
                    'file': SimpleUploadedFile('updated.pdf', b'updated', content_type='application/pdf'),
                },
                format='multipart',
            )

        self.assertEqual(response.status_code, 500, response.data)
        self.assertEqual(response.data['code'], 'storage_unavailable')

        document.refresh_from_db()
        self.assertEqual(document.title, 'Original')
        self.assertEqual(document.document_type, 'application_for_testing')

    def test_legacy_document_upload_returns_structured_storage_error(self):
        application = self._create_application('APP-LEGACY-001')

        with patch('django.core.files.storage.FileSystemStorage._save', side_effect=PermissionError('no write')):
            response = self.client.post(
                self.documents_url,
                data={
                    'title': 'Application',
                    'document_type': 'application_for_testing',
                    'application': application.id,
                    'is_mandatory': True,
                    'file': SimpleUploadedFile('application.pdf', b'application', content_type='application/pdf'),
                },
                format='multipart',
            )

        self.assertEqual(response.status_code, 500, response.data)
        self.assertEqual(response.data['code'], 'storage_unavailable')
        self.assertEqual(application.documents.filter(is_deleted=False).count(), 0)

    def test_audit_document_storage_reports_missing_files(self):
        application = self._create_application('APP-AUDIT-001')

        existing_document = Document.objects.create(
            title='Existing',
            document_type='application_for_testing',
            application=application,
            uploaded_by=self.user,
            is_mandatory=True,
            file=SimpleUploadedFile('existing.pdf', b'existing', content_type='application/pdf'),
        )
        missing_document = Document.objects.create(
            title='Missing',
            document_type='breeding_questionnaire',
            application=application,
            uploaded_by=self.user,
            is_mandatory=True,
            file='documents/2026/01/15/missing.pdf',
        )

        self.assertTrue(os.path.exists(existing_document.file.path))
        self.assertFalse(os.path.exists(os.path.join(self.media_dir.name, missing_document.file.name)))

        stdout = io.StringIO()
        call_command('audit_document_storage', '--application-id', str(application.id), stdout=stdout)
        output = stdout.getvalue()

        self.assertIn(f'{existing_document.id}\t{application.id}\tapplication_for_testing\tTrue', output)
        self.assertIn(f'{missing_document.id}\t{application.id}\tbreeding_questionnaire\tFalse', output)
        self.assertIn(f'Applications needing re-upload: {application.id}', output)

    def test_legacy_document_upload_requires_exactly_one_context(self):
        trial = Trial.objects.create(
            region=self.region,
            culture=self.culture,
            status='active',
            created_by=self.user,
            start_date=date(2026, 5, 1),
            year=2026,
        )
        application = self._create_application('APP-CONTEXT-001')

        response = self.client.post(
            self.documents_url,
            data={
                'title': 'Invalid',
                'document_type': 'other',
                'application': application.id,
                'trial': trial.id,
                'is_mandatory': False,
                'file': SimpleUploadedFile('invalid.pdf', b'invalid', content_type='application/pdf'),
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn('Exactly one of "application" or "trial" must be provided.', str(response.data))

    def test_minio_backed_document_returns_signed_file_url_and_redirects_download(self):
        application = self._create_application('APP-MINIO-001')

        with override_settings(MEDIA_BACKEND='minio'):
            response = self.client.post(
                self.documents_url,
                data={
                    'title': 'Application',
                    'document_type': 'application_for_testing',
                    'application': application.id,
                    'is_mandatory': True,
                    'file': SimpleUploadedFile('application.pdf', b'minio-content', content_type='application/pdf'),
                },
                format='multipart',
            )

            self.assertEqual(response.status_code, 201, response.data)
            self.assertIn(f'/api/documents/{response.data["id"]}/signed-download/', response.data['file'])

            download_response = self.client.get(f'/api/documents/{response.data["id"]}/download/')
            self.assertEqual(download_response.status_code, 302)
            self.assertIn(f'/api/documents/{response.data["id"]}/signed-download/', download_response['Location'])

            signed_url = urlsplit(download_response['Location'])
            signed_response = APIClient().get(f'{signed_url.path}?{signed_url.query}')
            self.assertEqual(signed_response.status_code, 200)
            self.assertEqual(b''.join(signed_response.streaming_content), b'minio-content')

    def test_document_list_returns_signed_file_url_for_minio_documents(self):
        application = self._create_application('APP-MINIO-LIST-001')

        with override_settings(MEDIA_BACKEND='minio'):
            create_response = self.client.post(
                self.documents_url,
                data={
                    'title': 'Application',
                    'document_type': 'application_for_testing',
                    'application': application.id,
                    'is_mandatory': True,
                    'file': SimpleUploadedFile('application.pdf', b'minio-list', content_type='application/pdf'),
                },
                format='multipart',
            )

            self.assertEqual(create_response.status_code, 201, create_response.data)

            list_response = self.client.get(self.documents_url, {'application': application.id})
            self.assertEqual(list_response.status_code, 200, list_response.data)
            self.assertEqual(list_response.data['count'], 1)
            self.assertIn(
                f'/api/documents/{create_response.data["id"]}/signed-download/',
                list_response.data['results'][0]['file'],
            )

    def test_download_falls_back_to_legacy_filesystem_when_primary_is_missing(self):
        application = self._create_application('APP-LEGACY-FALLBACK-001')
        file_name = 'documents/2026/01/15/legacy-only.pdf'
        legacy_path = os.path.join(self.legacy_media_dir.name, file_name)
        os.makedirs(os.path.dirname(legacy_path), exist_ok=True)
        with open(legacy_path, 'wb') as legacy_file:
            legacy_file.write(b'legacy-content')

        document = Document.objects.create(
            title='Legacy Only',
            document_type='application_for_testing',
            application=application,
            uploaded_by=self.user,
            is_mandatory=True,
            file=file_name,
        )

        with override_settings(MEDIA_BACKEND='minio'):
            detail_response = self.client.get(f'/api/documents/{document.id}/')
            self.assertEqual(detail_response.status_code, 200, detail_response.data)
            self.assertTrue(detail_response.data['file'].endswith('/media/documents/2026/01/15/legacy-only.pdf'))

            download_response = self.client.get(f'/api/documents/{document.id}/download/')
            self.assertEqual(download_response.status_code, 200)
            self.assertEqual(b''.join(download_response.streaming_content), b'legacy-content')

    def test_download_returns_structured_404_when_missing_in_primary_and_legacy(self):
        application = self._create_application('APP-MISSING-001')
        document = Document.objects.create(
            title='Missing',
            document_type='application_for_testing',
            application=application,
            uploaded_by=self.user,
            is_mandatory=True,
            file='documents/2026/01/15/missing-everywhere.pdf',
        )

        with override_settings(MEDIA_BACKEND='minio'):
            response = self.client.get(f'/api/documents/{document.id}/download/')

        self.assertEqual(response.status_code, 404, response.data)
        self.assertEqual(response.data['code'], 'file_not_found')

    def test_download_returns_storage_unavailable_when_primary_storage_raises(self):
        application = self._create_application('APP-MINIO-ERROR-001')
        document = Document.objects.create(
            title='Broken Storage',
            document_type='application_for_testing',
            application=application,
            uploaded_by=self.user,
            is_mandatory=True,
            file='documents/2026/01/15/broken-storage.pdf',
        )

        with override_settings(MEDIA_BACKEND='minio'):
            with patch('trials_app.storage.default_storage.exists', side_effect=OSError('minio down')):
                response = self.client.get(f'/api/documents/{document.id}/download/')

        self.assertEqual(response.status_code, 500, response.data)
        self.assertEqual(response.data['code'], 'storage_unavailable')
