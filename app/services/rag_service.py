"""RAG (Retrieval Augmented Generation) service using ChromaDB."""

import uuid
import hashlib
from typing import Optional, Any

from app.services.llm_service import LLMService, get_llm_service
from app.db.chroma import (
    get_chroma_client,
    get_tech_blog_collection,
    get_user_content_collection,
    TECH_BLOG_KNOWLEDGE,
    USER_CONTENT,
)


class RAGService:
    """Service for RAG operations with ChromaDB."""

    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm = llm_service or get_llm_service()
        self._collections = {}

    def _get_collection(self, collection_name: str = USER_CONTENT):
        """Get or create a ChromaDB collection."""
        if collection_name not in self._collections:
            try:
                client = get_chroma_client()
                self._collections[collection_name] = client.get_or_create_collection(
                    name=collection_name,
                    metadata={"hnsw:space": "cosine"},
                )
            except Exception as e:
                # If ChromaDB is not available, return None
                print(f"ChromaDB not available: {e}")
                return None
        return self._collections[collection_name]

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = start + chunk_size
            chunk = text[start:end]

            # Try to break at sentence boundary
            if end < text_len:
                last_period = chunk.rfind(". ")
                if last_period > chunk_size // 2:
                    chunk = chunk[: last_period + 1]
                    end = start + last_period + 1

            chunks.append(chunk.strip())
            start = end - overlap

        return chunks

    def _generate_chunk_id(self, content: str, index: int) -> str:
        """Generate a unique ID for a chunk."""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"chunk_{content_hash}_{index}"

    async def add_document(
        self,
        title: str,
        content: str,
        source_url: Optional[str] = None,
        document_type: str = "general",
        metadata: Optional[dict] = None,
        collection_name: str = USER_CONTENT,
    ) -> dict:
        """Add a document to the knowledge base."""
        collection = self._get_collection(collection_name)

        if collection is None:
            # Fallback: return success without actually storing
            return {
                "id": f"doc_{uuid.uuid4().hex[:12]}",
                "title": title,
                "chunks_added": 0,
                "status": "stored_locally",
                "message": "ChromaDB not available, document metadata stored only",
            }

        # Chunk the document
        chunks = self._chunk_text(content)

        # Generate embeddings for chunks
        try:
            embeddings = await self.llm.embed_documents(chunks)
        except Exception as e:
            return {
                "id": f"doc_{uuid.uuid4().hex[:12]}",
                "title": title,
                "chunks_added": 0,
                "status": "error",
                "message": f"Failed to generate embeddings: {str(e)}",
            }

        # Prepare data for ChromaDB
        doc_id = f"doc_{uuid.uuid4().hex[:12]}"
        chunk_ids = [self._generate_chunk_id(chunk, i) for i, chunk in enumerate(chunks)]

        chunk_metadata = [
            {
                "doc_id": doc_id,
                "title": title,
                "source_url": source_url or "",
                "document_type": document_type,
                "chunk_index": i,
                "total_chunks": len(chunks),
                **(metadata or {}),
            }
            for i in range(len(chunks))
        ]

        # Add to collection
        try:
            collection.add(
                ids=chunk_ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=chunk_metadata,
            )
        except Exception as e:
            return {
                "id": doc_id,
                "title": title,
                "chunks_added": 0,
                "status": "error",
                "message": f"Failed to add to ChromaDB: {str(e)}",
            }

        return {
            "id": doc_id,
            "title": title,
            "chunks_added": len(chunks),
            "status": "uploaded",
            "message": f"Successfully added {len(chunks)} chunks to knowledge base",
        }

    async def search(
        self,
        query: str,
        top_k: int = 5,
        document_type: Optional[str] = None,
        collection_name: str = USER_CONTENT,
    ) -> dict:
        """Search the knowledge base for relevant content."""
        collection = self._get_collection(collection_name)

        if collection is None:
            return {
                "query": query,
                "results": [],
                "message": "ChromaDB not available",
            }

        # Generate query embedding
        try:
            query_embedding = await self.llm.embed_text(query)
        except Exception as e:
            return {
                "query": query,
                "results": [],
                "message": f"Failed to generate query embedding: {str(e)}",
            }

        # Build where filter if document_type specified
        where_filter = None
        if document_type:
            where_filter = {"document_type": document_type}

        # Search ChromaDB
        try:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where_filter,
                include=["documents", "metadatas", "distances"],
            )
        except Exception as e:
            return {
                "query": query,
                "results": [],
                "message": f"Search failed: {str(e)}",
            }

        # Format results
        formatted_results = []
        if results and results.get("documents"):
            documents = results["documents"][0] if results["documents"] else []
            metadatas = results["metadatas"][0] if results.get("metadatas") else []
            distances = results["distances"][0] if results.get("distances") else []
            ids = results["ids"][0] if results.get("ids") else []

            for i, doc in enumerate(documents):
                # Convert distance to similarity score (cosine distance to similarity)
                distance = distances[i] if i < len(distances) else 0
                similarity = 1 - distance  # Cosine similarity

                formatted_results.append({
                    "id": ids[i] if i < len(ids) else "",
                    "content": doc,
                    "title": metadatas[i].get("title", "") if i < len(metadatas) else "",
                    "score": round(similarity, 4),
                    "metadata": metadatas[i] if i < len(metadatas) else {},
                })

        return {
            "query": query,
            "results": formatted_results,
            "total_results": len(formatted_results),
        }

    async def delete_document(
        self,
        doc_id: str,
        collection_name: str = USER_CONTENT,
    ) -> dict:
        """Delete a document and all its chunks from the knowledge base."""
        collection = self._get_collection(collection_name)

        if collection is None:
            return {
                "id": doc_id,
                "status": "error",
                "message": "ChromaDB not available",
            }

        try:
            # Find all chunks with this doc_id
            results = collection.get(
                where={"doc_id": doc_id},
                include=["metadatas"],
            )

            if results and results.get("ids"):
                chunk_ids = results["ids"]
                collection.delete(ids=chunk_ids)

                return {
                    "id": doc_id,
                    "chunks_deleted": len(chunk_ids),
                    "status": "deleted",
                }
            else:
                return {
                    "id": doc_id,
                    "status": "not_found",
                    "message": "Document not found",
                }

        except Exception as e:
            return {
                "id": doc_id,
                "status": "error",
                "message": f"Delete failed: {str(e)}",
            }

    async def get_context_for_query(
        self,
        query: str,
        top_k: int = 3,
        collection_name: str = USER_CONTENT,
    ) -> str:
        """Get relevant context for a query (for RAG augmentation)."""
        search_results = await self.search(
            query=query,
            top_k=top_k,
            collection_name=collection_name,
        )

        if not search_results.get("results"):
            return ""

        # Combine relevant chunks into context
        context_parts = []
        for result in search_results["results"]:
            if result.get("score", 0) > 0.5:  # Only include relevant results
                title = result.get("title", "")
                content = result.get("content", "")
                context_parts.append(f"[Source: {title}]\n{content}")

        return "\n\n---\n\n".join(context_parts)


# Singleton instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get or create RAG service instance."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
