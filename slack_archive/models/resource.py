"""Database models for resources and their mentions."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Resource(Base):
    """Model for storing external resources (e.g., URLs)."""
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(2048), unique=True, nullable=False)
    title = Column(String(255))
    content = Column(Text)
    summary = Column(Text)
    scrape_status = Column(String(20), nullable=False, default="pending")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)


class ResourceMention(Base):
    """Model for tracking mentions of resources in messages."""
    __tablename__ = "resource_mentions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String(255), ForeignKey("messages.message_id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("message_id", "resource_id", name="unique_message_resource"),
    )