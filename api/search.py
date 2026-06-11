"""
FastAPI endpoint for searching resources.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List, Optional

from api.dependencies import get_db
from database.models import Resource

router = APIRouter()


@router.get(
    "/search",
    response_model=dict,
    summary="Search resources by query",
    description="Search resources by title, content, or summary with pagination.",
)
def search_resources(
    q: str = Query(..., description="Search query (required)"),
    limit: int = Query(10, description="Maximum number of results", ge=1),
    offset: int = Query(0, description="Pagination offset", ge=0),
    db: Session = Depends(get_db),
):
    """
    Search resources by query with pagination.
    
    Args:
        q: Search query (required).
        limit: Maximum number of results (default: 10).
        offset: Pagination offset (default: 0).
        db: Database session.
        
    Returns:
        Paginated search results.
        
    Raises:
        HTTPException: 422 if `q` is missing or 500 for database errors.
    """
    try:
        # Query the Resource model for matches in title, content, or summary
        results = (
            db.query(Resource)
            .filter(
                or_(
                    Resource.title.ilike(f"%{q}%"),
                    Resource.content.ilike(f"%{q}%"),
                    Resource.summary.ilike(f"%{q}%"),
                )
            )
            .offset(offset)
            .limit(limit)
            .all()
        )
        
        # Get total count of matching resources
        total = (
            db.query(Resource)
            .filter(
                or_(
                    Resource.title.ilike(f"%{q}%"),
                    Resource.content.ilike(f"%{q}%"),
                    Resource.summary.ilike(f"%{q}%"),
                )
            )
            .count()
        )
        
        # Format response
        response = {
            "results": [
                {
                    "id": resource.id,
                    "url": resource.url,
                    "title": resource.title,
                    "summary": resource.summary,
                    "content": resource.content,
                }
                for resource in results
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )