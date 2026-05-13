from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from trials_app.models import SortRecord


VALID_TOKEN = "test-secret-token-1234567890abcdef"
URL_NAME = "internal-sort-by-patent-id"


@override_settings(TRIALS_WEBHOOK_TOKEN=VALID_TOKEN)
class InternalSortWebhookTests(TestCase):
    def setUp(self):
        self.record = SortRecord.objects.create(
            sort_id=999001,
            name="Old name",
            synced_at=timezone.now(),
        )
        self.url = reverse(URL_NAME, kwargs={"patent_sort_id": self.record.sort_id})

    def _patch(self, body, token=None):
        headers = {}
        if token is not None:
            headers["HTTP_AUTHORIZATION"] = f"Token {token}"
        return self.client.patch(
            self.url,
            data=body,
            content_type="application/json",
            **headers,
        )

    def test_missing_token_rejected(self):
        response = self._patch({"name": "New name"})
        self.assertEqual(response.status_code, 403)

    def test_wrong_token_rejected(self):
        response = self._patch({"name": "New name"}, token="wrong-token")
        self.assertEqual(response.status_code, 403)

    def test_valid_token_updates_record(self):
        before = self.record.synced_at
        response = self._patch({"name": "Brand new name"}, token=VALID_TOKEN)
        self.assertEqual(response.status_code, 200)
        self.record.refresh_from_db()
        self.assertEqual(self.record.name, "Brand new name")
        self.assertGreater(self.record.synced_at, before)

    def test_unknown_sort_id_is_no_op(self):
        url = reverse(URL_NAME, kwargs={"patent_sort_id": 424242})
        response = self.client.patch(
            url,
            data={"name": "Anything"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {VALID_TOKEN}",
        )
        self.assertEqual(response.status_code, 204)

    def test_empty_name_rejected(self):
        response = self._patch({"name": ""}, token=VALID_TOKEN)
        self.assertEqual(response.status_code, 400)

    def test_overlong_name_rejected(self):
        response = self._patch({"name": "x" * 300}, token=VALID_TOKEN)
        self.assertEqual(response.status_code, 400)


@override_settings(TRIALS_WEBHOOK_TOKEN="")
class InternalSortWebhookNoTokenConfiguredTests(TestCase):
    def test_no_token_configured_rejects_all(self):
        SortRecord.objects.create(sort_id=999002, name="Old")
        url = reverse(URL_NAME, kwargs={"patent_sort_id": 999002})
        response = self.client.patch(
            url,
            data={"name": "x"},
            content_type="application/json",
            HTTP_AUTHORIZATION="Token whatever",
        )
        self.assertEqual(response.status_code, 403)
