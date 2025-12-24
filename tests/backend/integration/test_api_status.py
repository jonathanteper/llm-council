"""
Integration tests for service metadata endpoint.

Tests FR-1.3: Service Metadata Endpoint
The /api/v1/status endpoint provides service information
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


class TestServiceMetadata:
    """Test service metadata endpoint."""

    def test_status_endpoint_returns_200(self):
        """
        Test-1.3.1: GET /api/v1/status returns 200.
        
        Verifies: FR-1.3 (Service Metadata Endpoint)
        
        Given: Backend API is running
        When: GET request to /api/v1/status
        Then: Returns 200 status code
        """
        # Act
        response = client.get("/api/v1/status")
        
        # Assert
        assert response.status_code == 200

    def test_response_contains_all_required_fields(self):
        """
        Test-1.3.2: Response contains all required fields.
        
        Verifies: FR-1.3 (Service Metadata Endpoint)
        
        Given: Backend API is running
        When: GET request to /api/v1/status
        Then: Response contains service, version, api_version, status, models, features
        """
        # Act
        response = client.get("/api/v1/status")
        data = response.json()
        
        # Assert
        assert "service" in data
        assert "version" in data
        assert "api_version" in data
        assert "status" in data
        assert "models" in data
        assert "features" in data

    def test_version_matches_package_version(self):
        """
        Test-1.3.3: Version matches package version.
        
        Verifies: FR-1.3 (Service Metadata Endpoint)
        
        Given: Backend API is running with v1.2
        When: GET request to /api/v1/status
        Then: Version is '1.2.0' and api_version is 'v1'
        """
        # Act
        response = client.get("/api/v1/status")
        data = response.json()
        
        # Assert
        assert data["version"] == "1.2.0"
        assert data["api_version"] == "v1"

    def test_models_list_matches_config(self):
        """
        Test-1.3.4: Models list matches config.
        
        Verifies: FR-1.3 (Service Metadata Endpoint)
        
        Given: Backend API with configured models
        When: GET request to /api/v1/status
        Then: Models section contains council and chairman lists
        """
        # Act
        response = client.get("/api/v1/status")
        data = response.json()
        
        # Assert
        assert "council" in data["models"]
        assert "chairman" in data["models"]
        assert isinstance(data["models"]["council"], list)
        assert isinstance(data["models"]["chairman"], str)
        assert len(data["models"]["council"]) > 0

    def test_status_is_healthy(self):
        """
        Test-1.3.5: Status is 'healthy'.
        
        Verifies: FR-1.3 (Service Metadata Endpoint)
        
        Given: Backend API is running normally
        When: GET request to /api/v1/status
        Then: Status field is 'healthy'
        """
        # Act
        response = client.get("/api/v1/status")
        data = response.json()
        
        # Assert
        assert data["status"] == "healthy"

    def test_features_section_complete(self):
        """
        Test-1.3.6: Features section is complete.
        
        Verifies: FR-1.3 (Service Metadata Endpoint)
        
        Given: Backend API with v1.2 features
        When: GET request to /api/v1/status
        Then: Features includes auth_required, streaming, versioned_api
        """
        # Act
        response = client.get("/api/v1/status")
        data = response.json()
        
        # Assert
        assert "auth_required" in data["features"]
        assert "streaming" in data["features"]
        assert "versioned_api" in data["features"]
        assert isinstance(data["features"]["auth_required"], bool)
        assert isinstance(data["features"]["streaming"], bool)
        assert isinstance(data["features"]["versioned_api"], bool)

    def test_service_name_correct(self):
        """
        Test-1.3.7: Service name is correct.
        
        Verifies: FR-1.3 (Service Metadata Endpoint)
        
        Given: Backend API is running
        When: GET request to /api/v1/status
        Then: Service name is 'LLM Council API'
        """
        # Act
        response = client.get("/api/v1/status")
        data = response.json()
        
        # Assert
        assert data["service"] == "LLM Council API"

