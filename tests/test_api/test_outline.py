"""Tests for outline API endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_generate_outline_success(client):
    """Test outline generation with valid request."""
    response = client.post(
        "/api/v1/outline",
        json={
            "topic": "Building REST APIs with FastAPI",
            "niche": "fullstack",
            "target_audience": "intermediate",
            "word_count": 2000,
            "include_code_examples": True,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "title" in data
    assert "sections" in data
    assert data["estimated_words"] == 2000


def test_generate_outline_minimal_request(client):
    """Test outline generation with minimal required fields."""
    response = client.post(
        "/api/v1/outline",
        json={
            "topic": "Python Basics",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "title" in data


def test_generate_outline_invalid_topic(client):
    """Test outline generation fails with short topic."""
    response = client.post(
        "/api/v1/outline",
        json={
            "topic": "ab",  # Too short (min 3 chars)
        },
    )

    assert response.status_code == 422  # Validation error


def test_generate_outline_invalid_word_count(client):
    """Test outline generation fails with invalid word count."""
    response = client.post(
        "/api/v1/outline",
        json={
            "topic": "Valid Topic",
            "word_count": 100,  # Below minimum of 500
        },
    )

    assert response.status_code == 422
