"""Integration tests for the summarization pipeline."""

import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from database.models import Resource
from scraping.scraper import scrape_content
from scraping.github_scraper import scrape_github_readme
from ai.summarizer import summarize_content, update_resource_summary


@pytest.fixture
def test_resource(db_session: Session) -> Resource:
    """Fixture to create a test resource in the database."""
    resource = Resource(
        url="https://github.com/test/repo",
        normalized_url="github.com/test/repo",
        title="Test Repo"
    )
    db_session.add(resource)
    db_session.commit()
    return resource


@pytest.fixture
def test_non_github_resource(db_session: Session) -> Resource:
    """Fixture to create a non-GitHub test resource in the database."""
    resource = Resource(
        url="https://example.com/article",
        normalized_url="example.com/article",
        title="Test Article"
    )
    db_session.add(resource)
    db_session.commit()
    return resource


def test_successful_pipeline_github(db_session: Session, test_resource: Resource):
    """Test successful summarization pipeline for a GitHub URL."""
    with patch("scraping.github_scraper.scrape_github_readme") as mock_scrape_github, \
         patch("ai.summarizer.summarize_content") as mock_summarize:
        
        # Mock successful scraping and summarization
        mock_scrape_github.return_value = "This is a test README content."
        mock_summarize.return_value = "This is a summary."
        
        # Simulate pipeline execution
        content = scrape_github_readme(test_resource.url)
        summary = summarize_content(content, "fake_api_key")
        update_resource_summary(db_session, test_resource.id, summary=summary)
        
        # Verify resource updates
        updated_resource = db_session.get(Resource, test_resource.id)
        assert updated_resource.content == "This is a test README content."
        assert updated_resource.summary == "This is a summary."
        assert updated_resource.summary_error is None
        assert updated_resource.scrape_failed is None


def test_successful_pipeline_non_github(db_session: Session, test_non_github_resource: Resource):
    """Test successful summarization pipeline for a non-GitHub URL."""
    with patch("scraping.scraper.scrape_content") as mock_scrape, \
         patch("ai.summarizer.summarize_content") as mock_summarize:
        
        # Mock successful scraping and summarization
        mock_scrape.return_value = "This is a test article content."
        mock_summarize.return_value = "This is a summary."
        
        # Simulate pipeline execution
        content = scrape_content(test_non_github_resource.url)
        summary = summarize_content(content, "fake_api_key")
        update_resource_summary(db_session, test_non_github_resource.id, summary=summary)
        
        # Verify resource updates
        updated_resource = db_session.get(Resource, test_non_github_resource.id)
        assert updated_resource.content == "This is a test article content."
        assert updated_resource.summary == "This is a summary."
        assert updated_resource.summary_error is None
        assert updated_resource.scrape_failed is None


def test_scraping_failure(db_session: Session, test_resource: Resource):
    """Test pipeline behavior when scraping fails."""
    with patch("scraping.github_scraper.scrape_github_readme") as mock_scrape_github:
        
        # Mock scraping failure
        mock_scrape_github.return_value = None
        
        # Simulate pipeline execution
        content = scrape_github_readme(test_resource.url)
        update_resource_summary(db_session, test_resource.id, error="Scraping failed")
        
        # Verify resource updates
        updated_resource = db_session.get(Resource, test_resource.id)
        assert updated_resource.content is None
        assert updated_resource.summary is None
        assert updated_resource.scrape_failed == "Scraping failed"


def test_summarization_failure(db_session: Session, test_resource: Resource):
    """Test pipeline behavior when summarization fails."""
    with patch("scraping.github_scraper.scrape_github_readme") as mock_scrape_github, \
         patch("ai.summarizer.summarize_content") as mock_summarize:
        
        # Mock successful scraping but failed summarization
        mock_scrape_github.return_value = "This is a test README content."
        mock_summarize.side_effect = Exception("API Error")
        
        # Simulate pipeline execution
        content = scrape_github_readme(test_resource.url)
        summary = summarize_content(content, "fake_api_key")
        update_resource_summary(db_session, test_resource.id, error="API Error")
        
        # Verify resource updates
        updated_resource = db_session.get(Resource, test_resource.id)
        assert updated_resource.content == "This is a test README content."
        assert updated_resource.summary is None
        assert updated_resource.summary_error == "API Error"