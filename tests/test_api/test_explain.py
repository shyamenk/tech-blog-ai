"""Tests for explain API endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_explain_concept_success(client):
    """Test concept explanation with valid request."""
    response = client.post(
        "/api/v1/explain",
        json={
            "concept": "Dependency Injection",
            "mode": "technical",
            "include_examples": True,
            "include_analogies": True,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["concept"] == "Dependency Injection"
    assert data["mode"] == "technical"
    assert "explanation" in data
    assert "examples" in data
    assert "analogies" in data


def test_explain_concept_eli5_mode(client):
    """Test concept explanation in ELI5 mode."""
    response = client.post(
        "/api/v1/explain",
        json={
            "concept": "Machine Learning",
            "mode": "eli5",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "eli5"


def test_explain_concept_invalid_short(client):
    """Test explanation fails with short concept."""
    response = client.post(
        "/api/v1/explain",
        json={
            "concept": "a",  # Too short
        },
    )

    assert response.status_code == 422
