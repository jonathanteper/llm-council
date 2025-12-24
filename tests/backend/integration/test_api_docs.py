"""
Integration tests for OpenAPI documentation.

Tests FR-3.2: OpenAPI/Swagger Documentation
FastAPI auto-generated docs at /api/v1/docs
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


class TestOpenAPIDocumentation:
    """Test OpenAPI/Swagger documentation."""

    def test_swagger_ui_accessible(self):
        """
        Test-3.2.1: /docs returns Swagger UI.
        
        Verifies: FR-3.2 (OpenAPI/Swagger Documentation)
        
        Given: Backend API is running
        When: GET request to /docs
        Then: Returns 200 with Swagger UI HTML
        """
        # Act
        response = client.get("/docs")
        
        # Assert
        assert response.status_code == 200
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower()

    def test_openapi_json_accessible(self):
        """
        Test-3.2.2: OpenAPI JSON schema accessible.
        
        Verifies: FR-3.2 (OpenAPI/Swagger Documentation)
        
        Given: Backend API is running
        When: GET request to /openapi.json
        Then: Returns 200 with valid OpenAPI schema
        """
        # Act
        response = client.get("/openapi.json")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data

    def test_all_v1_endpoints_documented(self):
        """
        Test-3.2.3: All API v1 endpoints documented.
        
        Verifies: FR-3.2 (OpenAPI/Swagger Documentation)
        
        Given: Backend API with v1 endpoints
        When: Examining OpenAPI schema
        Then: All /api/v1/ endpoints are documented
        """
        # Act
        response = client.get("/openapi.json")
        data = response.json()
        paths = data.get("paths", {})
        
        # Assert - Check key v1 endpoints are documented
        expected_paths = [
            "/api/v1/status",
            "/api/v1/conversations",
            "/api/v1/conversations/{conversation_id}",
            "/api/v1/conversations/{conversation_id}/message",
        ]
        
        for expected_path in expected_paths:
            assert expected_path in paths, f"Endpoint {expected_path} not documented"

    def test_api_title_and_version_in_schema(self):
        """
        Test-3.2.4: API title and version in OpenAPI schema.
        
        Verifies: FR-3.2 (OpenAPI/Swagger Documentation)
        
        Given: Backend API with metadata
        When: Examining OpenAPI schema
        Then: Title and version are present
        """
        # Act
        response = client.get("/openapi.json")
        data = response.json()
        
        # Assert
        assert "info" in data
        assert "title" in data["info"]
        assert "LLM Council" in data["info"]["title"]
        assert "version" in data["info"]

