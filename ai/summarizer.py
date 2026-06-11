"""AI summarization module using Groq's OpenAI-compatible SDK."""

from typing import Optional
from groq import Groq
from sqlalchemy.orm import Session

# Import Resource model (assuming it exists in the codebase)
from database.models import Resource

summary_error: Optional[str] = None


def summarize_content(content: Optional[str], api_key: str) -> Optional[str]:
    """Summarize content using Groq's SDK.
    
    Args:
        content: The content to summarize.
        api_key: Groq API key.
        
    Returns:
        Summary as a string if successful, None otherwise.
        Sets `summary_error` if summarization fails.
    """
    global summary_error
    client = Groq(api_key=api_key)
    
    if content is None:
        summary_error = "No content to summarize"
        return None

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": f"Summarize this content:\n\n{content}"}],
            max_tokens=150
        )
        summary_error = None
        return response.choices[0].message.content
    except Exception as e:
        summary_error = str(e)
        return None


def update_resource_summary(
    db_session: Session, 
    resource_id: int, 
    summary: Optional[str] = None, 
    error: Optional[str] = None
) -> None:
    """Update the Resource model with the summary or error.
    
    Args:
        db_session: SQLAlchemy database session.
        resource_id: ID of the resource to update.
        summary: Generated summary (optional).
        error: Error message (optional).
    """
    resource = db_session.get(Resource, resource_id)
    if not resource:
        return
    
    if summary:
        resource.summary = summary
    if error:
        resource.summary_error = error
    
    db_session.commit()