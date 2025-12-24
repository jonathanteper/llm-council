"""
Unit tests for API key authentication middleware.

Tests FR-1.2: Optional API Authentication
API keys via X-API-Key header (optional)
"""

import pytest
import os
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient


class TestAPIKeyAuthentication:
    """Test API key authentication middleware."""

    def test_auth_disabled_by_default(self):
        """
        Test-1.2.3: Request without API key succeeds (if auth disabled).
        
        Verifies: FR-1.2 (Optional API Authentication)
        
        Given: Backend with auth disabled (default)
        When: Request without X-API-Key header
        Then: Request succeeds
        """
        # Import here to get fresh app instance
        from backend.main import app
        client = TestClient(app)
        
        # Act
        response = client.get("/api/v1/conversations")
        
        # Assert - Should succeed since auth is optional
        assert response.status_code == 200

    def test_request_with_valid_api_key_succeeds(self):
        """
        Test-1.2.1: Request with valid API key succeeds.
        
        Verifies: FR-1.2 (Optional API Authentication)
        
        Given: Backend with API keys configured
        When: Request with valid X-API-Key header
        Then: Request succeeds with 200
        """
        # Set up environment with API keys
        os.environ["API_AUTH_ENABLED"] = "true"
        os.environ["API_KEYS"] = "test-key-1,test-key-2"
        
        # Import after env vars set
        from backend import config
        # Force reload config
        import importlib
        importlib.reload(config)
        from backend.main import app
        
        client = TestClient(app)
        
        # Act
        response = client.get(
            "/api/v1/conversations",
            headers={"X-API-Key": "test-key-1"}
        )
        
        # Assert
        assert response.status_code == 200
        
        # Cleanup
        del os.environ["API_AUTH_ENABLED"]
        del os.environ["API_KEYS"]

    def test_request_with_invalid_api_key_returns_401(self):
        """
        Test-1.2.2: Request with invalid API key returns 401.
        
        Verifies: FR-1.2 (Optional API Authentication)
        
        Given: Backend with API keys configured
        When: Request with invalid X-API-Key header
        Then: Request fails with 401 Unauthorized
        """
        # Set up environment with API keys
        os.environ["API_AUTH_ENABLED"] = "true"
        os.environ["API_KEYS"] = "test-key-1,test-key-2"
        
        # Import after env vars set
        from backend import config
        import importlib
        importlib.reload(config)
        from backend.main import app
        
        client = TestClient(app)
        
        # Act
        response = client.get(
            "/api/v1/conversations",
            headers={"X-API-Key": "invalid-key"}
        )
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "error" in data or "detail" in data
        
        # Cleanup
        del os.environ["API_AUTH_ENABLED"]
        del os.environ["API_KEYS"]

    def test_api_key_validation_is_case_sensitive(self):
        """
        Test-1.2.4: API key validation is case-sensitive.
        
        Verifies: FR-1.2 (Optional API Authentication)
        
        Given: Backend with API keys configured
        When: Request with wrong case API key
        Then: Request fails with 401
        """
        # Set up environment with API keys
        os.environ["API_AUTH_ENABLED"] = "true"
        os.environ["API_KEYS"] = "TestKey123"
        
        # Import after env vars set
        from backend import config
        import importlib
        importlib.reload(config)
        from backend.main import app
        
        client = TestClient(app)
        
        # Act - wrong case
        response = client.get(
            "/api/v1/conversations",
            headers={"X-API-Key": "testkey123"}
        )
        
        # Assert
        assert response.status_code == 401
        
        # Act - correct case
        response = client.get(
            "/api/v1/conversations",
            headers={"X-API-Key": "TestKey123"}
        )
        
        # Assert
        assert response.status_code == 200
        
        # Cleanup
        del os.environ["API_AUTH_ENABLED"]
        del os.environ["API_KEYS"]

