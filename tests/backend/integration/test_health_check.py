"""
Integration tests for health check endpoint.

Verifies: FR-1.3 (Backend Health Check)

Test Plan:
- Test-1.3.1: /health endpoint returns 200 status code
- Test-1.3.2: /health endpoint returns correct JSON structure
- Test-1.3.3: /health endpoint includes service status
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_health_endpoint_returns_200():
    """
    Test-1.3.1: /health endpoint returns 200 status code.
    
    Verifies: FR-1.3 (Backend Health Check)
    
    Given: FastAPI application is running
    When: GET request is made to /health endpoint
    Then: Response status code is 200
    """
    # Act
    response = client.get("/health")
    
    # Assert
    assert response.status_code == 200


def test_health_endpoint_returns_correct_structure():
    """
    Test-1.3.2: /health endpoint returns correct JSON structure.
    
    Verifies: FR-1.3 (Backend Health Check)
    
    Given: FastAPI application is running
    When: GET request is made to /health endpoint
    Then: Response contains 'status' and 'service' fields
    """
    # Act
    response = client.get("/health")
    data = response.json()
    
    # Assert
    assert "status" in data
    assert "service" in data


def test_health_endpoint_includes_service_status():
    """
    Test-1.3.3: /health endpoint includes service status.
    
    Verifies: FR-1.3 (Backend Health Check)
    
    Given: FastAPI application is running
    When: GET request is made to /health endpoint
    Then: Response status is 'healthy' and service name is present
    """
    # Act
    response = client.get("/health")
    data = response.json()
    
    # Assert
    assert data["status"] == "healthy"
    assert data["service"] == "LLM Council API"

