"""
Integration tests for Frontend Dockerfile.

Verifies: FR-2.1 (Frontend Dockerfile)

Test Plan:
- Test-2.1.1: Dockerfile exists and is readable
- Test-2.1.2: Docker image builds successfully
- Test-2.1.3: Container exposes port 5173
- Test-2.1.4: Container serves the application
- Test-2.1.5: Container includes Node.js and npm dependencies
"""

import pytest
import subprocess
import time
import requests
from pathlib import Path


def test_dockerfile_exists():
    """
    Test-2.1.1: Dockerfile exists and is readable.
    
    Verifies: FR-2.1 (Frontend Dockerfile)
    
    Given: Project repository structure
    When: Looking for frontend.Dockerfile
    Then: File exists and is readable
    """
    # Arrange
    dockerfile_path = Path(__file__).parent.parent.parent.parent / "frontend.Dockerfile"
    
    # Assert
    assert dockerfile_path.exists(), "frontend.Dockerfile not found"
    assert dockerfile_path.is_file(), "frontend.Dockerfile is not a file"
    
    # Verify it's readable
    content = dockerfile_path.read_text()
    assert len(content) > 0, "frontend.Dockerfile is empty"


@pytest.mark.integration
def test_docker_image_builds_successfully():
    """
    Test-2.1.2: Docker image builds successfully.
    
    Verifies: FR-2.1 (Frontend Dockerfile)
    
    Given: frontend.Dockerfile with valid configuration
    When: docker build command is executed
    Then: Image builds successfully with exit code 0
    """
    # Arrange
    project_root = Path(__file__).parent.parent.parent.parent
    dockerfile_path = project_root / "frontend.Dockerfile"
    
    # Act
    result = subprocess.run(
        ["docker", "build", "-f", str(dockerfile_path), "-t", "llm-council-frontend:test", "."],
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
def test_container_exposes_port_5173():
    """
    Test-2.1.3: Container exposes port 5173.
    
    Verifies: FR-2.1 (Frontend Dockerfile)
    
    Given: Built Docker image
    When: Image metadata is inspected
    Then: Port 5173 is exposed
    """
    # Act
    result = subprocess.run(
        ["docker", "image", "inspect", "llm-council-frontend:test"],
        capture_output=True,
        text=True
    )
    
    # Assert
    assert result.returncode == 0, "Failed to inspect Docker image"
    assert "5173" in result.stdout, "Port 5173 not exposed in Docker image"


@pytest.mark.integration
def test_container_serves_application():
    """
    Test-2.1.4: Container serves the application.
    
    Verifies: FR-2.1 (Frontend Dockerfile)
    
    Given: Running container from built image
    When: HTTP request is made to root endpoint
    Then: Vite dev server responds with HTML
    """
    # Arrange - Start container
    container_name = "llm-council-frontend-test"
    
    # Clean up any existing container
    subprocess.run(["docker", "rm", "-f", container_name], 
                   stderr=subprocess.DEVNULL)
    
    try:
        # Start container
        result = subprocess.run(
            [
                "docker", "run", "-d",
                "--name", container_name,
                "-p", "5174:5173",  # Use different host port to avoid conflicts
                "llm-council-frontend:test"
            ],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Failed to start container: {result.stderr}"
        
        # Wait for Vite to be ready (max 30 seconds)
        time.sleep(5)
        for _ in range(25):
            try:
                response = requests.get("http://localhost:5174", timeout=2)
                if response.status_code == 200:
                    break
            except requests.exceptions.RequestException:
                time.sleep(1)
        else:
            # Get container logs for debugging
            logs = subprocess.run(
                ["docker", "logs", container_name],
                capture_output=True,
                text=True
            )
            pytest.fail(f"Container did not become ready within 30 seconds. Logs:\n{logs.stdout}\n{logs.stderr}")
        
        # Act
        response = requests.get("http://localhost:5174", timeout=5)
        
        # Assert
        assert response.status_code == 200
        assert "<!doctype html>" in response.text.lower() or "<!DOCTYPE html>" in response.text
        assert "vite" in response.text.lower() or "root" in response.text
        
    finally:
        # Cleanup
        subprocess.run(["docker", "rm", "-f", container_name], 
                      stderr=subprocess.DEVNULL)


@pytest.mark.integration
def test_container_includes_node_and_dependencies():
    """
    Test-2.1.5: Container includes Node.js and npm dependencies.
    
    Verifies: FR-2.1 (Frontend Dockerfile)
    
    Given: Built Docker image
    When: Container is run with command to check Node and dependencies
    Then: Node.js is installed and dependencies are available
    """
    # Act - Check Node.js is installed
    result_node = subprocess.run(
        ["docker", "run", "--rm", "llm-council-frontend:test", "node", "--version"],
        capture_output=True,
        text=True
    )
    
    # Assert Node.js is installed
    assert result_node.returncode == 0, "Node.js not found in container"
    assert "v20" in result_node.stdout, "Node.js 20 not installed"
    
    # Act - Check npm is installed
    result_npm = subprocess.run(
        ["docker", "run", "--rm", "llm-council-frontend:test", "npm", "--version"],
        capture_output=True,
        text=True
    )
    
    # Assert npm is installed
    assert result_npm.returncode == 0, "npm not found in container"
    
    # Act - Check React is installed
    result_react = subprocess.run(
        ["docker", "run", "--rm", "--workdir", "/app", "llm-council-frontend:test",
         "node", "-e", "console.log(require('react').version)"],
        capture_output=True,
        text=True
    )
    
    # Assert React is installed
    assert result_react.returncode == 0, f"React not installed in container: {result_react.stderr}"

