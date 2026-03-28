"""
Regression tests for PatentsServiceClient pagination.

Verifies that query params (culture, group, search, etc.) are preserved
when fetching pages 2+ from Patents Service API.
"""

from unittest.mock import patch, call
import pytest
from trials_app.patents_integration import PatentsServiceClient


def _paginated_response(results, page, total, page_size=20):
    """Helper: build a paginated response dict."""
    has_next = page * page_size < total
    return {
        'count': total,
        'next': f'http://localhost:8000/api/v2/patents/sorts/?page={page + 1}' if has_next else None,
        'previous': None if page == 1 else f'...?page={page - 1}',
        'results': results,
    }


class TestPaginationPreservesParams:
    """Params passed to page 1 must also appear on page 2+."""

    def setup_method(self):
        self.client = PatentsServiceClient()

    @pytest.mark.parametrize(
        'method_name, filter_params, log_fragment',
        [
            ('get_all_sorts', {'culture': 11}, 'сортов'),
            ('get_all_cultures', {'group': 1}, 'культур'),
            ('get_all_group_cultures', {'search': 'зерн'}, 'групп культур'),
            ('get_all_originators', {'search': 'нии'}, 'оригинаторов'),
        ],
        ids=['sorts', 'cultures', 'group_cultures', 'originators'],
    )
    def test_filter_params_preserved_on_page_2(
        self, method_name, filter_params, log_fragment
    ):
        page1_items = [{'id': i, 'name': f'item_{i}'} for i in range(20)]
        page2_items = [{'id': i, 'name': f'item_{i}'} for i in range(20, 25)]

        def mock_request(method, endpoint, **kwargs):
            params = kwargs.get('params', {})
            page = params.get('page', 1) if params else 1
            if page == 1:
                return _paginated_response(page1_items, page=1, total=25)
            else:
                return _paginated_response(page2_items, page=2, total=25)

        with patch.object(self.client, '_make_request', side_effect=mock_request) as mock:
            method = getattr(self.client, method_name)
            result = method(params=filter_params)

            # Should have fetched both pages
            assert len(result) == 25

            # Page 2 call must include the original filter params
            page2_call = mock.call_args_list[1]
            page2_params = page2_call.kwargs.get('params') or page2_call[1].get('params', {})

            for key, value in filter_params.items():
                assert key in page2_params, (
                    f'{method_name}: filter param "{key}" lost on page 2. '
                    f'Got params: {page2_params}'
                )
                assert page2_params[key] == value

            assert page2_params.get('page') == 2

    @pytest.mark.parametrize(
        'method_name',
        ['get_all_sorts', 'get_all_cultures', 'get_all_group_cultures', 'get_all_originators'],
    )
    def test_single_page_works_without_params(self, method_name):
        """No crash when params=None and response fits in one page."""
        items = [{'id': i, 'name': f'item_{i}'} for i in range(5)]

        def mock_request(method, endpoint, **kwargs):
            return _paginated_response(items, page=1, total=5)

        with patch.object(self.client, '_make_request', side_effect=mock_request):
            method = getattr(self.client, method_name)
            result = method(params=None)
            assert len(result) == 5
