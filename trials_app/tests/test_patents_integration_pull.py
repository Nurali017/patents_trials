"""Regression tests for the patents_integration HTTP client.

These run under Django's stock test runner (no pytest dependency).
"""

from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from trials_app.patents_integration import PatentsServiceClient


class GetAllSortsEndpointSurfaceTests(SimpleTestCase):
    """get_all_sorts must not poke /sorts/all/ — it 404s on v2."""

    def setUp(self):
        self.client = PatentsServiceClient()

    def test_only_calls_sorts_slash_endpoint(self):
        called_endpoints = []

        def mock_request(method, endpoint, **kwargs):
            called_endpoints.append(endpoint)
            return {'count': 0, 'next': None, 'results': []}

        with patch.object(self.client, '_make_request', side_effect=mock_request):
            self.client.get_all_sorts({'culture': 5})

        self.assertEqual(called_endpoints, ['/sorts/'])
        self.assertTrue(all('all' not in ep for ep in called_endpoints))


class GetAuthTokenTests(SimpleTestCase):
    def setUp(self):
        self.client = PatentsServiceClient()
        self.client.service_username = 'svc'
        self.client.service_password = 'secret'
        self.client._token = None

    @patch('trials_app.patents_integration.requests.post')
    def test_returns_token_on_success(self, post):
        response = MagicMock(status_code=200)
        response.json.return_value = {'token': 'abc1234567890'}
        response.raise_for_status = lambda: None
        post.return_value = response

        token = self.client.get_auth_token()

        self.assertEqual(token, 'abc1234567890')
        called_url = post.call_args.args[0]
        self.assertTrue(called_url.endswith('/api/v1/auth/'))
        called_body = post.call_args.kwargs['data']
        self.assertEqual(called_body['username'], 'svc')
        self.assertEqual(called_body['password'], 'secret')

    @patch('trials_app.patents_integration.requests.post')
    def test_returns_none_on_400(self, post):
        import requests as _requests
        bad = MagicMock(status_code=400)
        bad.raise_for_status.side_effect = _requests.exceptions.HTTPError('400')
        post.return_value = bad

        self.assertIsNone(self.client.get_auth_token())

    def test_returns_none_when_credentials_unset(self):
        self.client.service_username = None
        self.client.service_password = None
        self.assertIsNone(self.client.get_auth_token())
