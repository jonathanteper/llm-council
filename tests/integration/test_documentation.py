"""
Tests for Documentation Quality (README).

Verifies: FR-5.1 (Docker Instructions in README), NFR-4.2 (Documentation Quality)

Test Plan:
- Test-5.1.1: README exists and is readable
- Test-5.1.2: README contains Docker instructions
- Test-5.1.3: README contains native workflow instructions
- Test-5.1.4: README contains troubleshooting section
"""

import pytest
from pathlib import Path


def test_readme_exists():
    """
    Test-5.1.1: README exists and is readable.
    
    Verifies: FR-5.1 (Docker Instructions in README)
    
    Given: Project repository
    When: Checking for README.md
    Then: File exists and has content
    """
    # Arrange
    readme = Path(__file__).parent.parent.parent / "README.md"
    
    # Assert
    assert readme.exists(), "README.md not found"
    assert readme.is_file(), "README.md is not a file"
    
    content = readme.read_text()
    assert len(content) > 100, "README.md is too short or empty"


def test_readme_has_docker_instructions():
    """
    Test-5.1.2: README contains Docker instructions.
    
    Verifies: FR-5.1 (Docker Instructions in README)
    
    Given: README.md file
    When: Content is reviewed
    Then: Docker setup and usage instructions are present
    """
    # Arrange
    readme = Path(__file__).parent.parent.parent / "README.md"
    content = readme.read_text().lower()
    
    # Assert - Docker instructions present
    assert "docker" in content, "Docker not mentioned in README"
    assert "docker compose up" in content, "docker compose up command not documented"
    assert "docker compose down" in content or "ctrl+c" in content, \
        "How to stop containers not documented"
    
    # Check for key Docker benefits/features
    assert "hot reload" in content, "Hot reload feature not documented"
    assert "localhost:5173" in content or "5173" in content, "Frontend URL not documented"


def test_readme_has_native_instructions():
    """
    Test-5.1.3: README contains native workflow instructions.
    
    Verifies: NFR-2.1 (Native Workflow Compatibility), FR-5.1
    
    Given: README.md file
    When: Content is reviewed
    Then: Native development instructions are preserved
    """
    # Arrange
    readme = Path(__file__).parent.parent.parent / "README.md"
    content = readme.read_text().lower()
    
    # Assert - Native workflow still documented
    assert "native" in content or "option 2" in content, \
        "Native workflow option not clearly marked"
    assert "uv run python -m backend.main" in content or "uv run" in content, \
        "Backend native startup not documented"
    assert "npm run dev" in content, "Frontend native startup not documented"
    assert "start.sh" in content, "start.sh script not documented"


def test_readme_has_prerequisites():
    """
    Test-5.1.2: README documents prerequisites.
    
    Verifies: NFR-4.2 (Documentation Quality)
    
    Given: README.md file
    When: Content is reviewed
    Then: Prerequisites for both Docker and native are documented
    """
    # Arrange
    readme = Path(__file__).parent.parent.parent / "README.md"
    content = readme.read_text().lower()
    
    # Assert - Prerequisites documented
    assert "prerequisite" in content or "install" in content or "setup" in content, \
        "Prerequisites section not clearly marked"
    assert ".env" in content, ".env file requirement not documented"
    assert "openrouter" in content or "api key" in content, \
        "OpenRouter API key requirement not documented"


def test_readme_has_troubleshooting():
    """
    Test-5.1.4: README contains troubleshooting section.
    
    Verifies: FR-5.1 (Documentation Quality)
    
    Given: README.md file
    When: Content is reviewed
    Then: Troubleshooting guidance is provided
    """
    # Arrange
    readme = Path(__file__).parent.parent.parent / "README.md"
    content = readme.read_text().lower()
    
    # Assert - Troubleshooting section present
    assert "troubleshoot" in content or "issues" in content or "problems" in content, \
        "Troubleshooting section not found"
    
    # Check for common issues documented
    assert "port" in content, "Port conflict troubleshooting not documented"


def test_readme_has_project_structure():
    """
    Verify README documents project structure.
    
    Verifies: NFR-4.2 (Documentation Quality)
    
    Given: README.md file
    When: Content is reviewed
    Then: Project structure is documented
    """
    # Arrange
    readme = Path(__file__).parent.parent.parent / "README.md"
    content = readme.read_text()
    
    # Assert - Project structure documented
    assert "backend/" in content, "Backend directory not documented"
    assert "frontend/" in content, "Frontend directory not documented"
    assert "docker-compose.yml" in content or "Docker" in content, \
        "Docker files not mentioned"

