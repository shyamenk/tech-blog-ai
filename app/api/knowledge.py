"""Knowledge base API endpoints."""

from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.models.requests import KnowledgeUploadRequest, KnowledgeSearchRequest
from app.models.responses import (
    KnowledgeUploadResponse,
    KnowledgeSearchResponse,
    KnowledgeSearchResult,
)
from app.services.rag_service import get_rag_service

router = APIRouter()


@router.post("/knowledge/upload", response_model=KnowledgeUploadResponse)
async def upload_document(request: KnowledgeUploadRequest) -> KnowledgeUploadResponse:
    """Upload a document to the knowledge base."""
    try:
        rag_service = get_rag_service()

        result = await rag_service.add_document(
            title=request.title,
            content=request.content,
            source_url=request.source_url,
            document_type=request.document_type,
            metadata=request.metadata,
        )

        return KnowledgeUploadResponse(
            id=result.get("id", "unknown"),
            title=request.title,
            status=result.get("status", "unknown"),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {str(e)}")


@router.post("/knowledge/search", response_model=KnowledgeSearchResponse)
async def search_knowledge(request: KnowledgeSearchRequest) -> KnowledgeSearchResponse:
    """Semantic search in the knowledge base."""
    try:
        rag_service = get_rag_service()

        result = await rag_service.search(
            query=request.query,
            top_k=request.top_k,
            document_type=request.document_type,
        )

        # Convert results to response format
        search_results = []
        for item in result.get("results", []):
            search_results.append(
                KnowledgeSearchResult(
                    id=item.get("id", ""),
                    title=item.get("title", ""),
                    content=item.get("content", ""),
                    score=item.get("score", 0.0),
                    metadata=item.get("metadata", {}),
                )
            )

        return KnowledgeSearchResponse(
            query=request.query,
            results=search_results,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.delete("/knowledge/{document_id}")
async def delete_document(document_id: str) -> dict:
    """Remove a document from the knowledge base."""
    try:
        rag_service = get_rag_service()

        result = await rag_service.delete_document(doc_id=document_id)

        if result.get("status") == "not_found":
            raise HTTPException(status_code=404, detail="Document not found")

        return {
            "id": document_id,
            "status": result.get("status", "unknown"),
            "message": result.get("message", "Document deleted"),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
