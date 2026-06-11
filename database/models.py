"""
SQLAlchemy models for the database.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Message(Base):
    """Represents a Slack message."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, nullable=False)
    text = Column(Text, nullable=False)
    author = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    channel = Column(String, nullable=False)

    # Relationship to ResourceMention
    resource_mentions = relationship("ResourceMention", back_populates="message")


class Resource(Base):
    """Represents an external resource (URL)."""
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    normalized_url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    summary_error = Column(String, nullable=True)  # Error if summarization fails, if any
    scrape_failed = Column(String, nullable=True)  # Reason for failure, if any
    ai_failed = Column(String, nullable=True)  # Reason for failure, if any

    # Relationship to ResourceMention
    resource_mentions = relationship("ResourceMention", back_populates="resource")


class ResourceMention(Base):
    """Represents a mention of a resource in a message."""
    __tablename__ = "resource_mentions"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)

    # Relationships
    message = relationship("Message", back_populates="resource_mentions")
    resource = relationship("Resource", back_populates="resource_mentions")

    # Composite unique constraint to avoid duplicate mentions
    __table_args__ = (
        UniqueConstraint("message_id", "resource_id", name="uq_message_resource"),
    )