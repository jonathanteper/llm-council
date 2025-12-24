"""
Integration tests for Backend Dockerfile.

Verifies: FR-1.1 (Backend Dockerfile)

Test Plan:
- Test-1.1.1: Dockerfile exists and is readable
- Test-1.1.2: Docker image builds successfully
- Test-1.1.3: Container exposes port 8001
- Test-1.1.4: Health check endpoint responds correctly
- Test-1.1.5: Container includes uv and Python dependencies
"""

import pytest
import subprocess
import time
import requests
from pathlib import Path


def test_dockerfile_exists():
    """
    Test-1.1.1: Dockerfile exists and is readable.
    
    Verifies: FR-1.1 (Backend Dockerfile)
    
    Given: Project repository structure
    When: Looking for backend.Dockerfile
    Then: File exists and is readable
    """
    # Arrange
    dockerfile_path = Path(__file__).parent.parent.parent.parent / "backend.Dockerfile"
    
    # Assert
    assert dockerfile_path.exists(), "backend.Dockerfile not found"
    assert dockerfile_path.is_file(), "backend.Dockerfile is not a file"
    
    # Verify it's readable
    content = dockerfile_path.read_text()
    assert len(content) > 0, "backend.Dockerfile is empty"


@pytest.mark.integration
def test_docker_image_builds_successfully():
    """
    Test-1.1.2: Docker image builds successfully.
    
    Verifies: FR-1.1 (Backend Dockerfile)
    
    Given: backend.Dockerfile with valid configuration
    When: docker build command is executed
    Then: Image builds successfully with exit code 0
    """
    # Arrange
    project_root = Path(__file__).parent.parent.parent.parent
    dockerfile_path = project_root / "backend.Dockerfile"
    
    # Act
    result = subprocess.run(
        ["docker", "build", "-f", str(dockerfile_path), "-t", "llm-council-backend:test", "."],
        cwd=str(project_root),
        capture_output=True,
        text=True,
        timeout=300  # 5 minutes max for build
    )
    
    # Assert
    assert result.returncode == 0, f"Docker build failed:\n{result.stderr}"
    # With BuildKit, success messages appear in stderr
    output = result.stdout + result.stderr
    assert "Successfully built" in output or "Successfully tagged" in output or "naming to docker.io" in output


@pytest.mark.integration
def test_container_exposes_port_8001():
    """
    Test-1.1.3: Container exposes port 8001.
    
    Verifies: FR-1.1 (Backend Dockerfile)
    
    Given: Built Docker image
    When: Image metadata is inspected
    Then: Port 8001 is exposed
    """
    # Act
    result = subprocess.run(
        ["docker", "image", "inspect", "llm-council-backend:test"],
        capture_output=True,
        text=True
    )
    
    # Assert
    assert result.returncode == 0, "Failed to inspect Docker image"
    assert "8001" in result.stdout, "Port 8001 not exposed in Docker image"


@pytest.mark.integration
def test_container_health_check_responds():
    """
    Test-1.1.4: Health check endpoint responds correctly in container.
    
    Verifies: FR-1.1 (Backend Dockerfile)
    
    Given: Running container from built image
    When: HTTP request is made to /health endpoint
    Then: Endpoint returns 200 OK with correct response
    """
    # Arrange - Start container
    container_name = "llm-council-backend-test"
    project_root = Path(__file__).parent.parent.parent.parent
    
    # Clean up any existing container
    subprocess.run(["docker", "rm", "-f", container_name], 
                   stderr=subprocess.DEVNULL)
    
    try:
        # Start container
        result = subprocess.run(
            [
                "docker", "run", "-d",
                "--name", container_name,
                "-p", "8001:8001",
                "-v", f"{project_root}/.env:/app/.env:ro",
                "llm-council-backend:test"
            ],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Failed to start container: {result.stderr}"
        
        # Wait for container to be ready (max 30 seconds)
        time.sleep(5)
        for _ in range(25):
            try:
                response = requests.get("http://localhost:8001/health", timeout=2)
                if response.status_code == 200:
                    break
            except requests.exceptions.RequestException:
                time.sleep(1)
        else:
            pytest.fail("Container did not become healthy within 30 seconds")
        
        # Act
        response = requests.get("http://localhost:8001/health", timeout=5)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "LLM Council API"
        
    finally:
        # Cleanup
        subprocess.run(["docker", "rm", "-f", container_name], 
                      stderr=subprocess.DEVNULL)


@pytest.mark.integration
def test_container_includes_uv_and_dependencies():
    """
    Test-1.1.5: Container includes uv and Python dependencies.
    
    Verifies: FR-1.1 (Backend Dockerfile)
    
    Given: Built Docker image
    When: Container is run with command to check uv and dependencies
    Then: uv is installed and dependencies are available
    """
    # Act - Check uv is installed
    result_uv = subprocess.run(
        ["docker", "run", "--rm", "llm-council-backend:test", "uv", "--version"],
        capture_output=True,
        text=True
    )
    
    # Assert uv is installed
    assert result_uv.returncode == 0, "uv package manager not found in container"
    assert "uv" in result_uv.stdout.lower(), "uv version not displayed"
    
    # Act - Check FastAPI is installed (use uv run to access venv)
    result_fastapi = subprocess.run(
        ["docker", "run", "--rm", "llm-council-backend:test", 
         "uv", "run", "python", "-c", "import fastapi; print(fastapi.__version__)"],
        capture_output=True,
        text=True
    )
    
    # Assert FastAPI is installed
    assert result_fastapi.returncode == 0, f"FastAPI not installed in container: {result_fastapi.stderr}"

