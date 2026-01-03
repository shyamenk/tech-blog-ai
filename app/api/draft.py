"""Draft writing API endpoints."""

from fastapi import APIRouter, HTTPException

from app.models.requests import DraftRequest
from app.models.responses import DraftResponse
from app.services.content_service import get_content_service

router = APIRouter()


@router.post("/draft", response_model=DraftResponse)
async def generate_draft(request: DraftRequest) -> DraftResponse:
    """Generate a full blog post draft using AI."""
    try:
        # Need either outline_id or topic
        if not request.outline_id and not request.topic:
            raise HTTPException(
                status_code=400,
                detail="Either outline_id or topic must be provided",
            )

        content_service = get_content_service()

        # TODO: If outline_id provided, fetch outline from database
        outline = None
        topic = request.topic or "Technical Blog Post"

        result = await content_service.generate_draft(
            topic=topic,
            outline=outline,
            tone=request.tone,
            word_count=request.word_count,
            include_code_examples=request.include_code_examples,
        )

        return DraftResponse(
            id=result.get("id", "draft_unknown"),
            title=result.get("title", topic),
            content=result.get("content", ""),
            word_count=result.get("word_count", 0),
            metadata=result.get("metadata", {}),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate draft: {str(e)}")
