"""Ingestion logic package."""
from .deduplication import (
    get_or_create_resource,
    create_resource_mention,
)

__all__ = [
    "get_or_create_resource",
    "create_resource_mention",
]