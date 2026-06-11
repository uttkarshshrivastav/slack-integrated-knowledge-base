"""
Unit tests for the generic web scraper.
"""
import pytest
from scraping.scraper import scrape_content
from unittest.mock import patch


@pytest.mark.parametrize(
    "html, expected_content",
    [
        ("<html><body><article>Test content</article></body></html>", "Test content"),
        ("<html><body></body></html>", None),
        ("", None),
    ],
)
def test_scrape_content(html, expected_content):
    """Tests scraping content from HTML."""
    with patch("trafilatura.fetch_url", return_value=html):
        with patch("trafilatura.extract", return_value=expected_content):
            assert scrape_content("https://example.com") == expected_content


def test_scrape_content_failure():
    """Tests scraping failure handling."""
    with patch("trafilatura.fetch_url", side_effect=Exception("Failed to fetch")):
        assert scrape_content("https://example.com") is None