"""
GitHub-specific scraper for fetching README content via GitHub API.
"""
import requests
from typing import Optional
from urllib.parse import urlparse


def is_github_url(url: str) -> bool:
    """
    Checks if a URL is a GitHub repository URL.

    Args:
        url: URL to check.

    Returns:
        True if the URL is a GitHub repository URL, False otherwise.
    """
    parsed = urlparse(url)
    return parsed.netloc == "github.com" and len(parsed.path.strip("/").split("/")) >= 2


def scrape_github_readme(url: str) -> Optional[str]:
    """
    Fetches the README content of a GitHub repository via GitHub API.

    Args:
        url: GitHub repository URL (e.g., https://github.com/user/repo).

    Returns:
        README content as a string, or None if fetching fails.
    """
    if not is_github_url(url):
        return None
        
    try:
        # Extract owner and repo from URL
        path_parts = urlparse(url).path.strip("/").split("/")
        owner, repo = path_parts[0], path_parts[1]
        
        # GitHub API URL for README
        api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
            
        # Fetch README content
        readme_data = response.json()
        download_url = readme_data.get("download_url")
        if not download_url:
            return None
            
        readme_response = requests.get(download_url, timeout=10)
        if readme_response.status_code != 200:
            return None
            
        return readme_response.text.strip()
    except Exception:
        return None