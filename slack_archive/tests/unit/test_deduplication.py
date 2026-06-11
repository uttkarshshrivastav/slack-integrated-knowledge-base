"""Unit tests for deduplication logic."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from slack_archive.models.resource import Base, Resource, ResourceMention
from slack_archive.ingestion.deduplication import (
    get_or_create_resource,
    create_resource_mention,
    process_message_resources,
)


@pytest.fixture(scope="module")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_get_or_create_resource_new(db_session):
    """Test creating a new resource."""
    url = "https://example.com"
    resource = get_or_create_resource(db_session, url, title="Example")
    
    assert resource.id is not None
    assert resource.url == url
    assert resource.title == "Example"


def test_get_or_create_resource_existing(db_session):
    """Test reusing an existing resource."""
    url = "https://example.com"
    existing_resource = get_or_create_resource(db_session, url, title="Example")
    
    # Attempt to create the same resource again
    resource = get_or_create_resource(db_session, url, title="New Title")
    
    assert resource.id == existing_resource.id
    assert resource.title == "Example"  # Title should not update


def test_create_resource_mention(db_session):
    """Test creating a resource mention."""
    resource = get_or_create_resource(db_session, "https://example.com")
    mention = create_resource_mention(db_session, "msg123", resource.id)
    
    assert mention.id is not None
    assert mention.message_id == "msg123"
    assert mention.resource_id == resource.id


def test_create_resource_mention_duplicate(db_session):
    """Test duplicate resource mention raises an error."""
    resource = get_or_create_resource(db_session, "https://example.com")
    create_resource_mention(db_session, "msg123", resource.id)
    
    with pytest.raises(ValueError, match="Mention for message_id=msg123 and resource_id=\d+ already exists"):
        create_resource_mention(db_session, "msg123", resource.id)


def test_process_message_resources(db_session):
    """Test processing resources in a message."""
    urls = ["https://example.com", "https://example.org"]
    resources = process_message_resources(db_session, "msg123", urls)
    
    assert len(resources) == 2
    assert {r.url for r in resources} == set(urls)


def test_process_message_resources_duplicate_url(db_session):
    """Test processing a message with duplicate URLs."""
    urls = ["https://example.com", "https://example.com"]
    resources = process_message_resources(db_session, "msg123", urls)
    
    assert len(resources) == 1
    assert resources[0].url == "https://example.com"


def test_process_message_resources_existing_mention(db_session):
    """Test processing a message with an existing mention."""
    url = "https://example.com"
    resource = get_or_create_resource(db_session, url)
    create_resource_mention(db_session, "msg123", resource.id)
    
    # Process the same message again
    resources = process_message_resources(db_session, "msg123", [url])
    
    assert len(resources) == 0  # No new resources created