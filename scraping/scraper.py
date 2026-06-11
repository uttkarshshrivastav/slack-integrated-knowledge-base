"""
Generic web scraper for extracting article text from HTML.
"""
import trafilatura
from typing import Optional


def scrape_content(url: str) -> Optional[str]:
    """
    Scrapes article text from a given URL using trafilatura.

    Args:
        url: URL to scrape.

    Returns:
        Extracted text as a string, or None if scraping fails.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return None
            
        content = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
        return content.strip() if content else None
    except Exception:
        return None