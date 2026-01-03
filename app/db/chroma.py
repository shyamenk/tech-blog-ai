"""ChromaDB vector database connection management."""

from typing import Optional

import chromadb
from chromadb import ClientAPI
from chromadb.config import Settings as ChromaSettings

from app.config import get_settings


# Collection names
TECH_BLOG_KNOWLEDGE = "tech_blog_knowledge"
SALESFORCE_DOCS = "salesforce_docs"
USER_CONTENT = "user_content"


class ChromaClient:
    """ChromaDB client manager."""

    _client: Optional[ClientAPI] = None

    @classmethod
    def create_client(cls) -> ClientAPI:
        """Create the ChromaDB client."""
        if cls._client is None:
            settings = get_settings()

            # Parse host and port from URL
            chroma_url = settings.chroma_url
            if chroma_url.startswith("http://"):
                chroma_url = chroma_url[7:]
            elif chroma_url.startswith("https://"):
                chroma_url = chroma_url[8:]

            parts = chroma_url.split(":")
            host = parts[0]
            port = int(parts[1]) if len(parts) > 1 else 8000

            cls._client = chromadb.HttpClient(
                host=host,
                port=port,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                ),
            )
        return cls._client

    @classmethod
    def get_client(cls) -> ClientAPI:
        """Get the ChromaDB client, creating it if necessary."""
        if cls._client is None:
            cls.create_client()
        return cls._client

    @classmethod
    def reset_client(cls) -> None:
        """Reset the client connection."""
        cls._client = None


def get_chroma_client() -> ClientAPI:
    """Dependency to get the ChromaDB client."""
    return ChromaClient.get_client()


def get_or_create_collection(name: str, metadata: Optional[dict] = None):
    """Get or create a ChromaDB collection."""
    client = ChromaClient.get_client()
    return client.get_or_create_collection(
        name=name,
        metadata=metadata or {"hnsw:space": "cosine"},
    )


def get_tech_blog_collection():
    """Get the tech blog knowledge collection."""
    return get_or_create_collection(
        TECH_BLOG_KNOWLEDGE,
        metadata={"description": "General tech documentation", "hnsw:space": "cosine"},
    )


def get_salesforce_collection():
    """Get the Salesforce docs collection."""
    return get_or_create_collection(
        SALESFORCE_DOCS,
        metadata={"description": "Salesforce/Apex references", "hnsw:space": "cosine"},
    )


def get_user_content_collection():
    """Get the user content collection."""
    return get_or_create_collection(
        USER_CONTENT,
        metadata={"description": "User uploaded documents", "hnsw:space": "cosine"},
    )
