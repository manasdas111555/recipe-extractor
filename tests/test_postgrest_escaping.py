"""
Unit tests for UPA-1222: PostgREST Parameter Escaping & Single-Column vs OR Filter Formatting
"""

from unittest.mock import patch, MagicMock
from backend.app.core.supabase_client import SupabaseRestClient


def test_postgrest_single_column_filter_escaping_unquoted():
    client = SupabaseRestClient(base_url="https://fake.supabase.co", service_role_key="fake_key")
    
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        # Single-column filter: classified_domain with reserved characters (%, _, (, ), comma, quote)
        client.list_extractions(domain="recipe_test%1(a,b)\"c")

        assert mock_get.called
        call_kwargs = mock_get.call_args.kwargs
        params = call_kwargs["params"]

        # Directive 4: Single-column filter must NOT double-quote value, but MUST escape %, _, (, ), comma, quotes
        expected_domain_param = r"ilike.*recipe\_test\%1\(a\,b\)\"c*"
        assert params["classified_domain"] == expected_domain_param


def test_postgrest_or_filter_escaping_double_quoted():
    client = SupabaseRestClient(base_url="https://fake.supabase.co", service_role_key="fake_key")
    
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        # OR filter: search_query with reserved characters
        client.list_extractions(search_query="samosa_test%1(a,b)\"c")

        assert mock_get.called
        call_kwargs = mock_get.call_args.kwargs
        params = call_kwargs["params"]

        # Directive 4: or=(...) values ARE double-quoted with escaped internal quotes as ""
        expected_or_param = f'(source_url.ilike.*"samosa\\_test\\%1\\(a\\,b\\)""c"*,raw_transcript.ilike.*"samosa\\_test\\%1\\(a\\,b\\)""c"*)'
        assert params["or"] == expected_or_param


def test_public_extraction_slug_filter_escaping_unquoted():
    client = SupabaseRestClient(base_url="https://fake.supabase.co", service_role_key="fake_key")
    
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "test-uuid"}]
        mock_get.return_value = mock_response

        client.get_public_extraction_by_slug_or_id("my-slug%test_1(a,b)\"c")

        assert mock_get.called
        call_kwargs = mock_get.call_args.kwargs
        params = call_kwargs["params"]

        # Single column filter slug=eq.<val> must NOT double-quote value
        expected_slug_param = r"eq.my-slug\%test\_1\(a\,b\)\"c"
        assert params["slug"] == expected_slug_param
