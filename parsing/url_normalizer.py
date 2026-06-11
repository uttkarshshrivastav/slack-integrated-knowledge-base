"""
Normalizes URLs by stripping tracking parameters and preserving meaningful parts.
"""
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
from typing import Dict, List


def _is_tracking_param(param: str) -> bool:
    """Checks if a query parameter is a tracking parameter."""
    tracking_params = {
        "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
        "fbclid", "gclid", "mc_cid", "mc_eid", "_ga", "__s", "mkt_tok"
    }
    return param.lower() in tracking_params


def normalize_url(url: str) -> str:
    """
    Normalizes a URL by:
    - Stripping tracking parameters (e.g., utm_*, fbclid).
    - Preserving fragments (#section) and non-tracking query parameters.

    Args:
        url: Input URL to normalize.

    Returns:
        Normalized URL as a string.
    """
    if not url:
        return url

    parsed = urlparse(url)
    
    # Handle fragments that contain query parameters (e.g., #section?utm_campaign=test)
    fragment_query = ""
    if parsed.fragment and "?" in parsed.fragment:
        fragment_parts = parsed.fragment.split("?", 1)
        fragment = fragment_parts[0]
        fragment_query = fragment_parts[1]
        
        # Parse fragment query parameters
        fragment_query_params = parse_qs(fragment_query)
        filtered_fragment_query: Dict[str, List[str]] = {}
        for param, values in fragment_query_params.items():
            if not _is_tracking_param(param):
                filtered_fragment_query[param] = values
        
        # Rebuild fragment
        if filtered_fragment_query:
            fragment_query = urlencode(filtered_fragment_query, doseq=True)
            fragment = f"{fragment}?{fragment_query}"
        else:
            fragment = fragment_parts[0]
    else:
        fragment = parsed.fragment

    # Handle main query parameters
    query_params = parse_qs(parsed.query)
    filtered_query: Dict[str, List[str]] = {}
    for param, values in query_params.items():
        if not _is_tracking_param(param):
            filtered_query[param] = values

    # Rebuild the URL
    new_query = urlencode(filtered_query, doseq=True)
    normalized_parsed = parsed._replace(query=new_query, fragment=fragment)
    return urlunparse(normalized_parsed)