"""
Extracts and deduplicates URLs from text using urlextract.
"""
from typing import List
from urlextract import URLExtract


def extract_urls(text: str) -> List[str]:
    """
    Extracts URLs from the given text and removes duplicates within the same message.

    Args:
        text: Input text containing URLs.

    Returns:
        List of unique URLs found in the text.
    """
    if not text:
        return []

    extractor = URLExtract()
    urls = extractor.find_urls(text)
    return list(set(urls))  # Remove duplicates within the same message