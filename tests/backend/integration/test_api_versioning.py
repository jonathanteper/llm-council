"""
Integration tests for API versioning.

Tests FR-2.1: Version Prefix
All API routes must be prefixed with /api/v1/
Old routes must be aliased for backward compatibility
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


class TestAPIVersioning:
    """Test API versioning implementation."""

    def test_versioned_conversations_list_endpoint(self):
        """
        Test-2.1.1: /api/v1/conversations returns 200.
        
        Verifies: FR-2.1 (Version Prefix)
        
        Given: Backend API is running
        When: GET request to /api/v1/conversations
        Then: Returns 200 status code
        """
        # Act
        response = client.get("/api/v1/conversations")
        
        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_versioned_conversation_create_endpoint(self):
        """
        Test-2.1.1b: /api/v1/conversations POST returns 200.
        
        Verifies: FR-2.1 (Version Prefix)
        
        Given: Backend API is running
        When: POST request to /api/v1/conversations
        Then: Returns 200 status code with conversation object
        """
        # Act
        response = client.post("/api/v1/conversations", json={})
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "messages" in data

    def test_versioned_conversation_get_endpoint(self):
        """
        Test-2.1.1c: /api/v1/conversations/{id} GET returns correct status.
        
        Verifies: FR-2.1 (Version Prefix)
        
        Given: Backend API is running
        When: GET request to /api/v1/conversations/{id}
        Then: Returns 404 for non-existent conversation
        """
        # Act
        response = client.get("/api/v1/conversations/non-existent-id")
        
        # Assert
        assert response.status_code == 404

    def test_old_route_still_works_for_backward_compatibility(self):
        """
        Test-2.1.2: /api/conversations still works (alias).
        
        Verifies: FR-2.1 (Version Prefix - Backward Compatibility)
        
        Given: Backend API is running with v1 routes
        When: GET request to old /api/conversations route
        Then: Returns 200 status code (aliased to v1 route)
        """
        # Act
        response = client.get("/api/conversations")
        
        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_old_route_create_conversation_still_works(self):
        """
        Test-2.1.2b: /api/conversations POST still works (alias).
        
        Verifies: FR-2.1 (Version Prefix - Backward Compatibility)
        
        Given: Backend API is running with v1 routes
        When: POST request to old /api/conversations route
        Then: Returns 200 status code with conversation
        """
        # Act
        response = client.post("/api/conversations", json={})
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "id" in data

    def test_all_v1_routes_have_prefix(self):
        """
        Test-2.1.3: All v1 routes have /api/v1/ prefix.
        
        Verifies: FR-2.1 (Version Prefix)
        
        Given: FastAPI application routes defined
        When: Inspecting route paths
        Then: All API routes have /api/v1/ prefix
        """
        # Get all routes from the FastAPI app
        api_routes = [
            route.path for route in app.routes 
            if hasattr(route, 'path') and route.path.startswith('/api/')
        ]
        
        # Filter out legacy alias routes
        v1_routes = [route for route in api_routes if '/api/v1/' in route]
        
        # All non-aliased API routes should have v1 prefix
        # (We allow old routes for backward compatibility)
        assert len(v1_routes) > 0, "No v1 routes found"
        
        # Verify key endpoints exist with v1 prefix
        expected_v1_routes = [
            "/api/v1/conversations",
            "/api/v1/conversations/{conversation_id}",
            "/api/v1/conversations/{conversation_id}/message",
        ]
        
        for expected_route in expected_v1_routes:
            matching_routes = [r for r in v1_routes if expected_route in r]
            assert len(matching_routes) > 0, f"Expected route {expected_route} not found in v1 routes"

    def test_versioned_send_message_endpoint(self):
        """
        Test-2.1.1d: /api/v1/conversations/{id}/message endpoint works.
        
        Verifies: FR-2.1 (Version Prefix)
        
        Given: A conversation exists
        When: POST request to /api/v1/conversations/{id}/message
        Then: Returns 404 for non-existent conversation
        """
        # Act
        response = client.post(
            "/api/v1/conversations/non-existent-id/message",
            json={"content": "test message"}
        )
        
        # Assert
        assert response.status_code == 404

    def test_root_and_health_endpoints_unversioned(self):
        """
        Test-2.1.3b: Root and health endpoints remain unversioned.
        
        Verifies: FR-2.1 (Version Prefix)
        
        Given: Backend API is running
        When: GET request to / and /health
        Then: Both return 200 (these are service endpoints, not API endpoints)
        """
        # Act - Root endpoint
        response = client.get("/")
        assert response.status_code == 200
        
        # Act - Health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

