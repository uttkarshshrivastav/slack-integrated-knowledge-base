"""Scraping logic package."""

import os
from typing import Optional
from database.models import Resource
from scraping.scraper import scrape_content
from scraping.github_scraper import scrape_github_readme, is_github_url
from ai.summarizer import summarize_content, update_resource_summary
import logging



def process_resource_content(db, resource: Resource) -> None:
    """
    Processes a resource's content by scraping its URL and updating the database.
    Handles edge cases like scraping failures and network errors gracefully.

    Args:
        db: Database session.
        resource: Resource object to process.
    """
    if resource.content or resource.scrape_failed:
        return  # Already processed or failed

    try:
        content: Optional[str] = None
        if is_github_url(resource.url):
            content = scrape_github_readme(resource.url)
        else:
            content = scrape_content(resource.url)

        if content:
            resource.content = content
            # Summarize content using AI
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                summary = summarize_content(content, api_key)
                update_resource_summary(db, resource.id, summary=summary, error=None)
            else:
                update_resource_summary(db, resource.id, summary=None, error="GROQ_API_KEY not set")
        else:
            resource.scrape_failed = "No content extracted"
            update_resource_summary(db, resource.id, summary=None, error="No content extracted")

    except Exception as e:
        logging.error(f"Failed to scrape {resource.url}: {str(e)}")
        resource.scrape_failed = str(e)
        update_resource_summary(db, resource.id, summary=None, error=str(e))

    db.commit()