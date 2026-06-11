"""
Unit tests for URL normalization logic.
"""
import pytest
from parsing.url_normalizer import normalize_url


@pytest.mark.parametrize(
    "url, expected_normalized_url",
    [
        (
            "https://example.com?utm_source=test",
            "https://example.com"
        ),
        (
            "https://example.com?param=value&utm_medium=test",
            "https://example.com?param=value"
        ),
        (
            "https://example.com#section?utm_campaign=test",
            "https://example.com#section"
        ),
        (
            "https://example.com/path?fbclid=123&param=value",
            "https://example.com/path?param=value"
        ),
        (
            "https://example.com/path?gclid=123",
            "https://example.com/path"
        ),
        (
            "https://example.com/path",
            "https://example.com/path"
        ),
        ("", ""),
        (None, None),
    ]
)
def test_normalize_url(url, expected_normalized_url):
    """Tests URL normalization for tracking parameters and fragments."""
    assert normalize_url(url) == expected_normalized_url