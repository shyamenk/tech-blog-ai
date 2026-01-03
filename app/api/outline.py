"""Outline generation API endpoints."""

from fastapi import APIRouter, HTTPException

from app.models.requests import OutlineRequest
from app.models.responses import OutlineResponse, OutlineSection
from app.services.content_service import get_content_service

router = APIRouter()


@router.post("/outline", response_model=OutlineResponse)
async def generate_outline(request: OutlineRequest) -> OutlineResponse:
    """Generate a blog post outline using AI."""
    try:
        content_service = get_content_service()
        result = await content_service.generate_outline(
            topic=request.topic,
            niche=request.niche,
            target_audience=request.target_audience,
            word_count=request.word_count,
            include_code_examples=request.include_code_examples,
        )

        # Convert sections to proper format
        sections = []
        for section in result.get("sections", []):
            if isinstance(section, dict):
                sections.append(
                    OutlineSection(
                        title=section.get("title", ""),
                        points=section.get("points", []),
                        has_code_example=section.get("has_code_example", False),
                    )
                )

        return OutlineResponse(
            id=result.get("id", "outline_unknown"),
            title=result.get("title", f"Guide to {request.topic}"),
            hook=result.get("hook", ""),
            sections=sections,
            estimated_words=result.get("estimated_words", request.word_count),
            seo_suggestions=result.get("seo_suggestions", {}),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate outline: {str(e)}")
