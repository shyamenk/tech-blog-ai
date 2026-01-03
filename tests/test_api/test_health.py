"""Tests for health check endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint returns healthy status."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "Tech Blog AI"
    assert "version" in data


def test_health_check_contains_version(client):
    """Test health check includes version info."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "1.0.0"
