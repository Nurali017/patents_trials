from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from unittest.mock import patch

from trials_app.models import Culture, GroupCulture, SortRecord
from trials_app.patents_integration import PatentsServiceHTTPError


class SortRecordCreateTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='sort-create-user',
            password='sort-create-pass',
        )
        self.client.force_authenticate(self.user)

        self.group = GroupCulture.objects.create(
            group_culture_id=1,
            name='Крупяные культуры',
        )
        self.culture = Culture.objects.create(
            culture_id=12,
            name='рис',
            group_culture=self.group,
        )
        self.url = '/api/sort-records/'

    @patch('trials_app.views.sort.patents_api.create_sort')
    def test_duplicate_patents_code_rejected_without_local_fallback(self, create_sort):
        create_sort.side_effect = PatentsServiceHTTPError(
            409,
            {
                'error_code': 'duplicate_code',
                'message': 'Сорт с таким кодом уже существует в данной культуре',
                'details': {
                    'field': 'code',
                    'existing_code': 'ВНИИР 10177',
                    'culture': 'рис',
                },
            },
            '',
        )

        response = self.client.post(
            self.url,
            {
                'name': 'Новый рис',
                'code': 'ВНИИР 10177',
                'patents_culture_id': self.culture.culture_id,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('code', response.data)
        self.assertEqual(SortRecord.objects.count(), 0)

    @patch('trials_app.views.sort.patents_api.create_sort')
    def test_successful_patents_create_persists_real_patents_id(self, create_sort):
        create_sort.return_value = {
            'id': 12345,
            'name': 'Новый рис',
            'code': 'RICE-1',
        }

        response = self.client.post(
            self.url,
            {
                'name': 'Новый рис',
                'code': 'RICE-1',
                'patents_culture_id': self.culture.culture_id,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['sort_id'], 12345)
        self.assertTrue(SortRecord.objects.filter(sort_id=12345).exists())
