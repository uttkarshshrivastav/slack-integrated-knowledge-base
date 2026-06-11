"""
Handles deduplication of resources and their mentions in messages.
"""
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from database.models import Resource, ResourceMention
from scraping.scraper import scrape_content
from scraping.github_scraper import scrape_github_readme, is_github_url


def get_or_create_resource(
    db: Session, url: str, normalized_url: str
) -> Resource:
    """
    Gets an existing resource by normalized URL or creates a new one.
    Processes the resource content after creation.

    Args:
        db: Database session.
        url: Original URL.
        normalized_url: Normalized URL.

    Returns:
        Resource object.
    """
    resource = db.query(Resource).filter_by(normalized_url=normalized_url).first()
    if not resource:
        resource = Resource(url=url, normalized_url=normalized_url)
        db.add(resource)
        db.commit()
        db.refresh(resource)
        
    # Process resource content after creation or retrieval
    from scraping import process_resource_content
    process_resource_content(db, resource)
    
    return resource


def create_resource_mention(
    db: Session, message_id: int, resource_id: int
) -> Optional[ResourceMention]:
    """
    Creates a mention of a resource in a message if it doesn't already exist.

    Args:
        db: Database session.
        message_id: ID of the message.
        resource_id: ID of the resource.

    Returns:
        ResourceMention object if created, None if already exists.
    """
    mention = (
        db.query(ResourceMention)
        .filter_by(message_id=message_id, resource_id=resource_id)
        .first()
    )
    if not mention:
        mention = ResourceMention(message_id=message_id, resource_id=resource_id)
        db.add(mention)
        db.commit()
        db.refresh(mention)
        return mention
    return None