"""
Integration tests for API response headers.

Tests FR-2.2: Version in Response Headers
All API responses must include version headers
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


class TestAPIHeaders:
    """Test API response headers."""

    def test_response_includes_api_version_header(self):
        """
        Test-2.2.1: Response includes X-API-Version header.
        
        Verifies: FR-2.2 (Version in Response Headers)
        
        Given: Backend API is running
        When: GET request to any API endpoint
        Then: Response includes X-API-Version header with value 'v1'
        """
        # Act
        response = client.get("/api/v1/conversations")
        
        # Assert
        assert "X-API-Version" in response.headers
        assert response.headers["X-API-Version"] == "v1"

    def test_response_includes_service_version_header(self):
        """
        Test-2.2.2: Response includes X-Service-Version header.
        
        Verifies: FR-2.2 (Version in Response Headers)
        
        Given: Backend API is running
        When: GET request to any API endpoint
        Then: Response includes X-Service-Version header with semantic version
        """
        # Act
        response = client.get("/api/v1/conversations")
        
        # Assert
        assert "X-Service-Version" in response.headers
        # Should be in format X.Y.Z
        version = response.headers["X-Service-Version"]
        parts = version.split(".")
        assert len(parts) == 3, f"Version should be X.Y.Z format, got {version}"

    def test_version_values_are_correct(self):
        """
        Test-2.2.3: Version values are correct.
        
        Verifies: FR-2.2 (Version in Response Headers)
        
        Given: Backend API is running with v1.2
        When: GET request to any API endpoint
        Then: API version is 'v1' and service version is '1.2.0'
        """
        # Act
        response = client.get("/api/v1/conversations")
        
        # Assert
        assert response.headers["X-API-Version"] == "v1"
        assert response.headers["X-Service-Version"] == "1.2.0"

    def test_all_endpoints_include_version_headers(self):
        """
        Test-2.2.4: All API endpoints include version headers.
        
        Verifies: FR-2.2 (Version in Response Headers)
        
        Given: Multiple API endpoints exist
        When: Requests made to different endpoints
        Then: All responses include version headers
        """
        # Test different endpoints
        endpoints = [
            "/",
            "/health",
            "/api/v1/conversations",
            "/api/conversations",  # Legacy route
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert "X-API-Version" in response.headers, f"Endpoint {endpoint} missing X-API-Version"
            assert "X-Service-Version" in response.headers, f"Endpoint {endpoint} missing X-Service-Version"

    def test_version_headers_on_post_requests(self):
        """
        Test-2.2.5: POST requests also include version headers.
        
        Verifies: FR-2.2 (Version in Response Headers)
        
        Given: Backend API is running
        When: POST request to API endpoint
        Then: Response includes version headers
        """
        # Act
        response = client.post("/api/v1/conversations", json={})
        
        # Assert
        assert response.status_code == 200
        assert "X-API-Version" in response.headers
        assert "X-Service-Version" in response.headers
        assert response.headers["X-API-Version"] == "v1"
        assert response.headers["X-Service-Version"] == "1.2.0"

    def test_version_headers_on_error_responses(self):
        """
        Test-2.2.6: Error responses also include version headers.
        
        Verifies: FR-2.2 (Version in Response Headers)
        
        Given: Backend API is running
        When: Request to non-existent conversation (404 error)
        Then: Error response still includes version headers
        """
        # Act
        response = client.get("/api/v1/conversations/non-existent-id")
        
        # Assert
        assert response.status_code == 404
        assert "X-API-Version" in response.headers
        assert "X-Service-Version" in response.headers

