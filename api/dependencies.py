"""Database session dependency for FastAPI."""
from sqlalchemy.orm import Session
from database.session import SessionLocal


def get_db() -> Session:
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()