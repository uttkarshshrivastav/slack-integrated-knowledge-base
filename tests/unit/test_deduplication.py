"""
Unit tests for resource deduplication logic.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Resource, ResourceMention
from slack_archive.ingestion.deduplication import (
    get_or_create_resource,
    create_resource_mention,
)


# Setup in-memory SQLite database for testing
@pytest.fixture(scope="module")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_get_or_create_resource(db_session):
    """Tests getting or creating a resource by normalized URL."""
    url = "https://example.com"
    normalized_url = "https://example.com"

    # Test creating a new resource
    resource = get_or_create_resource(db_session, url, normalized_url)
    assert resource.url == url
    assert resource.normalized_url == normalized_url
    assert resource.id is not None

    # Test retrieving an existing resource
    existing_resource = get_or_create_resource(db_session, url, normalized_url)
    assert existing_resource.id == resource.id


def test_create_resource_mention(db_session):
    """Tests creating a resource mention."""
    url = "https://example.com"
    normalized_url = "https://example.com"
    resource = get_or_create_resource(db_session, url, normalized_url)

    # Test creating a new mention
    mention = create_resource_mention(db_session, 1, resource.id)
    assert mention is not None
    assert mention.message_id == 1
    assert mention.resource_id == resource.id

    # Test duplicate mention
    duplicate_mention = create_resource_mention(db_session, 1, resource.id)
    assert duplicate_mention is None