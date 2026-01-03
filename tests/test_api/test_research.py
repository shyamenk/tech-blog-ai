"""Tests for research API endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_research_topic_success(client):
    """Test topic research with valid request."""
    response = client.post(
        "/api/v1/research",
        json={
            "topic": "LangChain RAG Implementation",
            "niche": "ai",
            "depth": "medium",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["topic"] == "LangChain RAG Implementation"
    assert "findings" in data
    assert "sources" in data


def test_research_topic_minimal(client):
    """Test research with minimal required fields."""
    response = client.post(
        "/api/v1/research",
        json={
            "topic": "FastAPI Tutorial",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "FastAPI Tutorial"


def test_get_research_not_found(client):
    """Test getting non-existent research session."""
    response = client.get("/api/v1/research/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
