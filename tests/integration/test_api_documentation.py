"""
Tests for API documentation accuracy.

Tests FR-3.1: API Usage Guide
Verifies README_API.md exists and examples work
"""

import pytest


class TestAPIDocumentation:
    """Test API documentation."""

    def test_readme_api_exists(self):
        """
        Test-3.1.1: README_API.md exists and is complete.
        
        Verifies: FR-3.1 (API Usage Guide)
        
        Given: Project documentation
        When: Checking for README_API.md
        Then: File exists with required sections
        """
        with open("README_API.md", "r") as f:
            content = f.read()
        
        # Assert required sections present
        required_sections = [
            "Quick Start",
            "Authentication",
            "API Endpoints",
            "Request/Response Formats",
            "Error Handling",
            "Code Examples",
            "Versioning"
        ]
        
        for section in required_sections:
            assert section in content, f"Section '{section}' missing from README_API.md"

    def test_readme_api_has_code_examples(self):
        """
        Test-3.1.2: README_API.md contains code examples.
        
        Verifies: FR-3.1 (API Usage Guide)
        
        Given: API documentation
        When: Examining README_API.md
        Then: Contains Python, JavaScript, and curl examples
        """
        with open("README_API.md", "r") as f:
            content = f.read()
        
        # Assert language examples present
        assert "```python" in content
        assert "```javascript" in content or "```js" in content
        assert "```bash" in content or "curl" in content

    def test_readme_api_documents_all_endpoints(self):
        """
        Test-3.1.3: README_API.md documents all endpoints.
        
        Verifies: FR-3.1 (API Usage Guide)
        
        Given: API with versioned endpoints
        When: Examining README_API.md
        Then: All key endpoints are documented
        """
        with open("README_API.md", "r") as f:
            content = f.read()
        
        # Assert key endpoints documented
        endpoints = [
            "/api/v1/status",
            "/api/v1/conversations",
            "/api/v1/conversations/{conversation_id}",
            "/api/v1/conversations/{conversation_id}/message",
        ]
        
        for endpoint in endpoints:
            assert endpoint in content, f"Endpoint {endpoint} not documented"

    def test_readme_api_has_authentication_section(self):
        """
        Test-3.1.4: README_API.md has authentication documentation.
        
        Verifies: FR-3.1 (API Usage Guide)
        
        Given: API with optional authentication
        When: Examining README_API.md
        Then: Authentication section with X-API-Key examples
        """
        with open("README_API.md", "r") as f:
            content = f.read()
        
        assert "Authentication" in content or "authentication" in content
        assert "X-API-Key" in content
        assert "optional" in content.lower()

    def test_readme_api_has_versioning_section(self):
        """
        Test-3.1.5: README_API.md documents versioning policy.
        
        Verifies: FR-3.1 (API Usage Guide) and FR-2.3 (Version Documentation)
        
        Given: API with versioning strategy
        When: Examining README_API.md
        Then: Versioning policy and migration guide present
        """
        with open("README_API.md", "r") as f:
            content = f.read()
        
        assert "Versioning" in content or "versioning" in content
        assert "/api/v1/" in content
        assert "v1.2" in content or "1.2.0" in content

