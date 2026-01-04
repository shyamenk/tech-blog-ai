"""PostgreSQL repository for data persistence."""

from typing import Optional, Any
from uuid import UUID
import json

from app.db.postgres import fetch_one, fetch_all, execute_query, PostgresPool


class BlogPostRepository:
    """Repository for blog post operations."""

    @staticmethod
    async def create(
        title: str,
        content: str,
        outline: Optional[dict] = None,
        niche: Optional[str] = None,
        target_audience: Optional[str] = None,
        word_count: Optional[int] = None,
        seo_metadata: Optional[dict] = None,
        status: str = "draft",
        user_id: Optional[UUID] = None,
    ) -> dict:
        """Create a new blog post."""
        query = """
            INSERT INTO blog_posts
            (title, content, outline, niche, target_audience, word_count, seo_metadata, status, user_id, slug)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING id, title, slug, status, created_at
        """
        # Generate slug from title
        slug = title.lower().replace(" ", "-").replace(":", "")[:100]

        outline_json = json.dumps(outline) if outline else None
        seo_json = json.dumps(seo_metadata) if seo_metadata else None

        row = await fetch_one(
            query, title, content, outline_json, niche, target_audience,
            word_count, seo_json, status, user_id, slug
        )

        return dict(row) if row else {}

    @staticmethod
    async def get_by_id(post_id: UUID) -> Optional[dict]:
        """Get a blog post by ID."""
        query = "SELECT * FROM blog_posts WHERE id = $1"
        row = await fetch_one(query, post_id)
        return dict(row) if row else None

    @staticmethod
    async def get_by_slug(slug: str) -> Optional[dict]:
        """Get a blog post by slug."""
        query = "SELECT * FROM blog_posts WHERE slug = $1"
        row = await fetch_one(query, slug)
        return dict(row) if row else None

    @staticmethod
    async def list_posts(
        status: Optional[str] = None,
        niche: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict]:
        """List blog posts with optional filters."""
        conditions = []
        params = []
        param_idx = 1

        if status:
            conditions.append(f"status = ${param_idx}")
            params.append(status)
            param_idx += 1

        if niche:
            conditions.append(f"niche = ${param_idx}")
            params.append(niche)
            param_idx += 1

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        query = f"""
            SELECT id, title, slug, status, niche, word_count, created_at, updated_at
            FROM blog_posts
            {where_clause}
            ORDER BY created_at DESC
            LIMIT ${param_idx} OFFSET ${param_idx + 1}
        """
        params.extend([limit, offset])

        rows = await fetch_all(query, *params)
        return [dict(row) for row in rows]

    @staticmethod
    async def update_status(post_id: UUID, status: str) -> bool:
        """Update blog post status."""
        query = "UPDATE blog_posts SET status = $1 WHERE id = $2"
        result = await execute_query(query, status, post_id)
        return "UPDATE 1" in result

    @staticmethod
    async def delete(post_id: UUID) -> bool:
        """Delete a blog post."""
        query = "DELETE FROM blog_posts WHERE id = $1"
        result = await execute_query(query, post_id)
        return "DELETE 1" in result


class ResearchSessionRepository:
    """Repository for research session operations."""

    @staticmethod
    async def create(
        topic: str,
        findings: dict,
        sources: Optional[list] = None,
        user_id: Optional[UUID] = None,
    ) -> dict:
        """Create a new research session."""
        query = """
            INSERT INTO research_sessions (topic, findings, sources, user_id)
            VALUES ($1, $2, $3, $4)
            RETURNING id, topic, created_at
        """
        findings_json = json.dumps(findings)
        sources_json = json.dumps(sources) if sources else None

        row = await fetch_one(query, topic, findings_json, sources_json, user_id)
        return dict(row) if row else {}

    @staticmethod
    async def get_by_id(session_id: UUID) -> Optional[dict]:
        """Get a research session by ID."""
        query = "SELECT * FROM research_sessions WHERE id = $1"
        row = await fetch_one(query, session_id)
        if row:
            result = dict(row)
            if result.get("findings"):
                result["findings"] = json.loads(result["findings"]) if isinstance(result["findings"], str) else result["findings"]
            if result.get("sources"):
                result["sources"] = json.loads(result["sources"]) if isinstance(result["sources"], str) else result["sources"]
            return result
        return None

    @staticmethod
    async def list_by_topic(topic: str, limit: int = 10) -> list[dict]:
        """List research sessions by topic (partial match)."""
        query = """
            SELECT id, topic, created_at
            FROM research_sessions
            WHERE topic ILIKE $1
            ORDER BY created_at DESC
            LIMIT $2
        """
        rows = await fetch_all(query, f"%{topic}%", limit)
        return [dict(row) for row in rows]


class KnowledgeDocumentRepository:
    """Repository for knowledge document operations."""

    @staticmethod
    async def create(
        title: str,
        content: str,
        embedding_id: str,
        source_url: Optional[str] = None,
        document_type: str = "general",
        metadata: Optional[dict] = None,
        user_id: Optional[UUID] = None,
    ) -> dict:
        """Create a new knowledge document record."""
        query = """
            INSERT INTO knowledge_documents
            (title, content, embedding_id, source_url, document_type, metadata, user_id)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id, title, embedding_id, document_type, created_at
        """
        metadata_json = json.dumps(metadata) if metadata else None

        row = await fetch_one(
            query, title, content, embedding_id, source_url,
            document_type, metadata_json, user_id
        )
        return dict(row) if row else {}

    @staticmethod
    async def get_by_embedding_id(embedding_id: str) -> Optional[dict]:
        """Get a document by its embedding ID."""
        query = "SELECT * FROM knowledge_documents WHERE embedding_id = $1"
        row = await fetch_one(query, embedding_id)
        return dict(row) if row else None

    @staticmethod
    async def delete_by_embedding_id(embedding_id: str) -> bool:
        """Delete a document by its embedding ID."""
        query = "DELETE FROM knowledge_documents WHERE embedding_id = $1"
        result = await execute_query(query, embedding_id)
        return "DELETE 1" in result

    @staticmethod
    async def list_documents(
        document_type: Optional[str] = None,
        limit: int = 50,
    ) -> list[dict]:
        """List knowledge documents."""
        if document_type:
            query = """
                SELECT id, title, source_url, document_type, created_at
                FROM knowledge_documents
                WHERE document_type = $1
                ORDER BY created_at DESC
                LIMIT $2
            """
            rows = await fetch_all(query, document_type, limit)
        else:
            query = """
                SELECT id, title, source_url, document_type, created_at
                FROM knowledge_documents
                ORDER BY created_at DESC
                LIMIT $1
            """
            rows = await fetch_all(query, limit)

        return [dict(row) for row in rows]


class WorkflowRunRepository:
    """Repository for tracking workflow runs."""

    @staticmethod
    async def create_table_if_not_exists():
        """Create workflow_runs table if it doesn't exist."""
        query = """
            CREATE TABLE IF NOT EXISTS workflow_runs (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                topic VARCHAR(500) NOT NULL,
                status VARCHAR(50) DEFAULT 'in_progress',
                workflow_type VARCHAR(50) DEFAULT 'blog',
                input_params JSONB,
                result JSONB,
                blog_post_id UUID REFERENCES blog_posts(id),
                research_session_id UUID REFERENCES research_sessions(id),
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                error TEXT
            )
        """
        await execute_query(query)

    @staticmethod
    async def create(
        topic: str,
        workflow_type: str = "blog",
        input_params: Optional[dict] = None,
    ) -> dict:
        """Create a new workflow run."""
        query = """
            INSERT INTO workflow_runs (topic, workflow_type, input_params, status)
            VALUES ($1, $2, $3, 'in_progress')
            RETURNING id, topic, status, started_at
        """
        params_json = json.dumps(input_params) if input_params else None
        row = await fetch_one(query, topic, workflow_type, params_json)
        return dict(row) if row else {}

    @staticmethod
    async def update_completed(
        run_id: UUID,
        status: str,
        result: Optional[dict] = None,
        blog_post_id: Optional[UUID] = None,
        research_session_id: Optional[UUID] = None,
        error: Optional[str] = None,
    ) -> bool:
        """Update workflow run as completed."""
        query = """
            UPDATE workflow_runs
            SET status = $1, result = $2, blog_post_id = $3,
                research_session_id = $4, error = $5, completed_at = CURRENT_TIMESTAMP
            WHERE id = $6
        """
        result_json = json.dumps(result) if result else None
        await execute_query(
            query, status, result_json, blog_post_id,
            research_session_id, error, run_id
        )
        return True

    @staticmethod
    async def get_by_id(run_id: UUID) -> Optional[dict]:
        """Get a workflow run by ID."""
        query = "SELECT * FROM workflow_runs WHERE id = $1"
        row = await fetch_one(query, run_id)
        return dict(row) if row else None
