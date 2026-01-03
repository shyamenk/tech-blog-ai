"""Response models for API endpoints."""

from typing import Any, Optional
from pydantic import BaseModel, Field


class ResearchFinding(BaseModel):
    """A single research finding."""

    title: str
    content: str
    confidence: float = Field(ge=0.0, le=1.0)
    source: Optional[str] = None


class ResearchResponse(BaseModel):
    """Response model for topic research."""

    id: str
    topic: str
    findings: list[ResearchFinding] = []
    sources: list[str] = []


class OutlineSection(BaseModel):
    """A section in the blog outline."""

    title: str
    points: list[str] = []
    has_code_example: bool = False


class OutlineResponse(BaseModel):
    """Response model for outline generation."""

    id: str
    title: str
    hook: str
    sections: list[OutlineSection] = []
    estimated_words: int
    seo_suggestions: dict[str, Any] = {}


class ExplainResponse(BaseModel):
    """Response model for concept explanation."""

    concept: str
    explanation: str
    examples: list[str] = []
    analogies: list[str] = []
    mode: str


class DraftResponse(BaseModel):
    """Response model for draft generation."""

    id: str
    title: str
    content: str
    word_count: int
    metadata: dict[str, Any] = {}


class SEOSuggestion(BaseModel):
    """An SEO suggestion."""

    type: str
    message: str
    priority: str = "medium"


class SEOResponse(BaseModel):
    """Response model for SEO optimization."""

    optimized_content: str
    keywords: list[str] = []
    meta_description: str
    suggestions: list[SEOSuggestion] = []


class KnowledgeUploadResponse(BaseModel):
    """Response model for knowledge base upload."""

    id: str
    title: str
    status: str


class KnowledgeSearchResult(BaseModel):
    """A single search result."""

    id: str
    title: str
    content: str
    score: float
    metadata: dict[str, Any] = {}


class KnowledgeSearchResponse(BaseModel):
    """Response model for knowledge base search."""

    query: str
    results: list[KnowledgeSearchResult] = []
