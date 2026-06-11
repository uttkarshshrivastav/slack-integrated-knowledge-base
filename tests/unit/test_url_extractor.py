"""
Unit tests for URL extraction logic.
"""
import pytest
from parsing.url_extractor import extract_urls


@pytest.mark.parametrize(
    "text, expected_urls",
    [
        ("Check this: https://example.com", ["https://example.com"]),
        (
            "Links: https://example.com and http://test.org",
            ["https://example.com", "http://test.org"]
        ),
        (
            "Duplicate: https://example.com and https://example.com",
            ["https://example.com"]
        ),
        ("No URLs here", []),
        ("", []),
        (None, []),
    ]
)
def test_extract_urls(text, expected_urls):
    """Tests URL extraction and deduplication."""
    assert set(extract_urls(text)) == set(expected_urls)