from unittest.mock import patch

from django.test import TestCase

from trials_app.models import Culture, GroupCulture


class PatentsCatalogAliasesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group_culture = GroupCulture.objects.create(
            group_culture_id=701,
            name='Cereals',
            code='cereals',
        )
        cls.culture = Culture.objects.create(
            culture_id=9101,
            name='Spring Wheat',
            code='wheat',
            group_culture=cls.group_culture,
        )

    @patch('trials_app.views.document.patents_api.get_all_group_cultures')
    def test_group_cultures_alias_uses_local_read_model(self, get_all_group_cultures):
        response = self.client.get('/api/patents/group-cultures/')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]['id'], 701)
        self.assertEqual(payload[0]['local_id'], self.group_culture.id)
        self.assertEqual(payload[0]['cultures_count'], 1)
        self.assertEqual(payload[0]['name'], 'Cereals')
        self.assertIn('created_at', payload[0])
        self.assertIn('updated_at', payload[0])
        get_all_group_cultures.assert_not_called()

    @patch('trials_app.views.document.patents_api.get_all_group_cultures')
    def test_group_culture_detail_alias_uses_local_read_model(self, get_all_group_cultures):
        response = self.client.get(f'/api/patents/group-cultures/{self.group_culture.group_culture_id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.group_culture.group_culture_id)
        self.assertEqual(response.json()['local_id'], self.group_culture.id)
        get_all_group_cultures.assert_not_called()

    @patch('trials_app.views.document.patents_api.get_all_cultures')
    def test_cultures_alias_filters_by_external_group_id(self, get_all_cultures):
        response = self.client.get('/api/patents/cultures/', {'group': self.group_culture.group_culture_id})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]['id'], self.culture.culture_id)
        self.assertEqual(payload[0]['local_id'], self.culture.id)
        self.assertEqual(payload[0]['patents_culture_id'], self.culture.culture_id)
        self.assertEqual(payload[0]['culture_group'], self.group_culture.group_culture_id)
        self.assertEqual(payload[0]['group_culture_id'], self.group_culture.group_culture_id)
        self.assertEqual(payload[0]['culture_group_name'], 'Cereals')
        self.assertIn('created_at', payload[0])
        self.assertIn('updated_at', payload[0])
        get_all_cultures.assert_not_called()

    @patch('trials_app.views.document.patents_api.get_culture')
    def test_culture_detail_alias_uses_local_read_model_with_external_id(self, get_culture):
        response = self.client.get(f'/api/patents/cultures/{self.culture.culture_id}/')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['id'], self.culture.culture_id)
        self.assertEqual(payload['patents_culture_id'], self.culture.culture_id)
        self.assertEqual(payload['local_id'], self.culture.id)
        get_culture.assert_not_called()

    def test_originators_correct_spelling_alias_is_registered(self):
        response = self.client.get('/api/patents/originators/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
