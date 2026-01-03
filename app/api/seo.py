"""SEO optimization API endpoints."""

from fastapi import APIRouter, HTTPException

from app.models.requests import SEOOptimizeRequest
from app.models.responses import SEOResponse, SEOSuggestion
from app.services.content_service import get_content_service

router = APIRouter()


@router.post("/seo/optimize", response_model=SEOResponse)
async def optimize_seo(request: SEOOptimizeRequest) -> SEOResponse:
    """Optimize content for SEO using AI."""
    try:
        content_service = get_content_service()
        result = await content_service.optimize_seo(
            content=request.content,
            keywords=request.keywords,
            target_audience=request.target_audience,
        )

        # Convert suggestions to proper format
        suggestions = []
        for suggestion in result.get("suggestions", []):
            if isinstance(suggestion, dict):
                suggestions.append(
                    SEOSuggestion(
                        type=suggestion.get("type", "general"),
                        message=suggestion.get("message", ""),
                        priority=suggestion.get("priority", "medium"),
                    )
                )

        # Handle keywords - could be dict or list
        keywords = result.get("keywords", [])
        if isinstance(keywords, dict):
            # Flatten keyword dict to list
            flat_keywords = []
            if "primary" in keywords:
                flat_keywords.append(keywords["primary"])
            if "secondary" in keywords:
                flat_keywords.extend(keywords["secondary"])
            if "long_tail" in keywords:
                flat_keywords.extend(keywords["long_tail"])
            keywords = flat_keywords

        return SEOResponse(
            optimized_content=result.get("optimized_content", request.content),
            keywords=keywords,
            meta_description=result.get("meta_description", ""),
            suggestions=suggestions,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to optimize SEO: {str(e)}")
