"""Request models for API endpoints."""

from typing import Optional
from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    """Request model for topic research."""

    topic: str = Field(..., min_length=3, max_length=500, description="Topic to research")
    niche: Optional[str] = Field(
        None, description="Content niche (salesforce, fullstack, ai)"
    )
    depth: str = Field(
        "medium", description="Research depth: shallow, medium, deep"
    )


class OutlineRequest(BaseModel):
    """Request model for outline generation."""

    topic: str = Field(..., min_length=3, max_length=500, description="Blog post topic")
    niche: Optional[str] = Field(
        None, description="Content niche (salesforce, fullstack, ai)"
    )
    target_audience: str = Field(
        "intermediate", description="Target audience: beginner, intermediate, advanced"
    )
    word_count: int = Field(
        2000, ge=500, le=10000, description="Target word count"
    )
    include_code_examples: bool = Field(
        True, description="Include code examples in outline"
    )


class ExplainRequest(BaseModel):
    """Request model for concept explanation."""

    concept: str = Field(..., min_length=2, max_length=300, description="Concept to explain")
    mode: str = Field(
        "technical", description="Explanation mode: eli5, technical, deep-dive"
    )
    include_examples: bool = Field(True, description="Include code examples")
    include_analogies: bool = Field(True, description="Include analogies")


class DraftRequest(BaseModel):
    """Request model for draft generation."""

    outline_id: Optional[str] = Field(None, description="ID of existing outline to use")
    topic: Optional[str] = Field(None, description="Topic if no outline_id provided")
    tone: str = Field(
        "conversational", description="Writing tone: conversational, formal, tutorial"
    )
    word_count: int = Field(
        2000, ge=500, le=10000, description="Target word count"
    )
    include_code_examples: bool = Field(True, description="Include code examples")


class SEOOptimizeRequest(BaseModel):
    """Request model for SEO optimization."""

    content: str = Field(..., min_length=100, description="Content to optimize")
    keywords: Optional[list[str]] = Field(None, description="Target keywords")
    target_audience: Optional[str] = Field(None, description="Target audience")


class KnowledgeUploadRequest(BaseModel):
    """Request model for knowledge base upload."""

    title: str = Field(..., min_length=3, max_length=500, description="Document title")
    content: str = Field(..., min_length=10, description="Document content")
    source_url: Optional[str] = Field(None, description="Source URL if applicable")
    document_type: str = Field(
        "general", description="Document type: general, salesforce, fullstack, ai"
    )
    metadata: Optional[dict] = Field(None, description="Additional metadata")


class KnowledgeSearchRequest(BaseModel):
    """Request model for knowledge base search."""

    query: str = Field(..., min_length=3, max_length=500, description="Search query")
    top_k: int = Field(5, ge=1, le=20, description="Number of results to return")
    document_type: Optional[str] = Field(None, description="Filter by document type")
