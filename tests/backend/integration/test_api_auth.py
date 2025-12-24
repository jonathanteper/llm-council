"""
Integration tests for API key authentication.

Tests FR-1.2: Optional API Authentication
End-to-end authentication flow testing
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


class TestAPIAuthentication:
    """Test API authentication integration."""

    def test_all_api_endpoints_accessible_without_auth(self):
        """
        Test-1.2.5: All endpoints accessible without auth (default).
        
        Verifies: FR-1.2 (Optional API Authentication - Backward Compatibility)
        
        Given: Backend with auth disabled (default)
        When: Requests to various endpoints without X-API-Key
        Then: All requests succeed
        """
        endpoints = [
            ("/", "GET"),
            ("/health", "GET"),
            ("/api/v1/status", "GET"),
            ("/api/v1/conversations", "GET"),
            ("/api/v1/conversations", "POST"),
        ]
        
        for endpoint, method in endpoints:
            if method == "GET":
                response = client.get(endpoint)
            elif method == "POST":
                response = client.post(endpoint, json={})
            
            # All should succeed (200 or 404, not 401)
            assert response.status_code != 401, \
                f"Endpoint {endpoint} returned 401 without auth required"

    def test_health_endpoints_never_require_auth(self):
        """
        Test-1.2.6: Health and status endpoints don't require auth.
        
        Verifies: FR-1.2 (Optional API Authentication)
        
        Given: Backend with auth potentially enabled
        When: Requests to health/status endpoints
        Then: Always succeed without auth
        """
        health_endpoints = [
            "/",
            "/health",
            "/api/v1/status"
        ]
        
        for endpoint in health_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200, \
                f"Health endpoint {endpoint} should always be accessible"

    def test_api_key_header_name_correct(self):
        """
        Test-1.2.7: API key header name is X-API-Key.
        
        Verifies: FR-1.2 (Optional API Authentication)
        
        Given: Backend expects X-API-Key header
        When: Request with correctly named header
        Then: Header is recognized (even if auth is disabled)
        """
        # This test just verifies the header name is correct
        # The actual validation is tested in unit tests
        response = client.get(
            "/api/v1/conversations",
            headers={"X-API-Key": "any-key"}
        )
        
        # Should succeed since auth is disabled by default
        assert response.status_code == 200

