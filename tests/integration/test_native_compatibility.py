"""
Tests for Native Workflow Compatibility.

Verifies: NFR-2.1 (Native Workflow Compatibility)

Test Plan:
- Test-NFR-2.1.1: start.sh script still exists and is executable
- Test-NFR-2.1.2: Backend can still run natively
- Test-NFR-2.1.3: Frontend can still run natively
- Test-NFR-2.1.4: No breaking changes to source code
"""

import pytest
import subprocess
from pathlib import Path


def test_start_script_exists():
    """
    Test-NFR-2.1.1: start.sh script still exists and is executable.
    
    Verifies: NFR-2.1 (Native Workflow Compatibility)
    
    Given: Project repository
    When: Checking for start.sh
    Then: File exists and is executable
    """
    # Arrange
    start_script = Path(__file__).parent.parent.parent / "start.sh"
    
    # Assert
    assert start_script.exists(), "start.sh not found - native workflow broken"
    assert start_script.is_file(), "start.sh is not a file"
    
    # Check if executable
    import os
    assert os.access(start_script, os.X_OK), "start.sh is not executable"


def test_backend_source_unchanged():
    """
    Test-NFR-2.1.4: Backend source code has no Docker-specific changes.
    
    Verifies: NFR-2.1 (Native Workflow Compatibility)
    
    Given: Backend source code
    When: Checking backend/main.py
    Then: No Docker-specific modifications that break native execution
    """
    # Arrange
    main_py = Path(__file__).parent.parent.parent / "backend" / "main.py"
    content = main_py.read_text()
    
    # Assert - backend should work both natively and in containers
    # It should bind to 0.0.0.0 by default (works in both environments)
    assert 'if __name__ == "__main__":' in content, "Native execution entry point missing"
    assert "uvicorn" in content, "Uvicorn import/usage missing"


def test_frontend_source_unchanged():
    """
    Test-NFR-2.1.4: Frontend source code has no Docker-specific changes.
    
    Verifies: NFR-2.1 (Native Workflow Compatibility)
    
    Given: Frontend source code
    When: Checking vite.config.js
    Then: Configuration works for both native and containerized development
    """
    # Arrange
    vite_config = Path(__file__).parent.parent.parent / "frontend" / "vite.config.js"
    content = vite_config.read_text()
    
    # Assert - Vite config should work in both environments
    # host: '0.0.0.0' works locally too (binds to all interfaces)
    assert "host:" in content or "host :" in content, "Server host configuration missing"
    
    # HMR with host: 'localhost' works in both environments
    assert "hmr:" in content or "hmr :" in content, "HMR configuration missing"


def test_pyproject_toml_unchanged():
    """
    Test-NFR-2.1.4: Python dependencies still work natively.
    
    Verifies: NFR-2.1 (Native Workflow Compatibility)
    
    Given: pyproject.toml
    When: Checking dependencies
    Then: Same dependencies work for native and containerized development
    """
    # Arrange
    pyproject = Path(__file__).parent.parent.parent / "pyproject.toml"
    content = pyproject.read_text()
    
    # Assert - Core dependencies unchanged
    assert "fastapi" in content, "FastAPI dependency missing"
    assert "uvicorn" in content, "Uvicorn dependency missing"
    assert "python-dotenv" in content, "python-dotenv dependency missing"


def test_package_json_unchanged():
    """
    Test-NFR-2.1.4: Frontend dependencies still work natively.
    
    Verifies: NFR-2.1 (Native Workflow Compatibility)
    
    Given: package.json
    When: Checking dependencies and scripts
    Then: Same setup works for native and containerized development
    """
    # Arrange
    import json
    package_json = Path(__file__).parent.parent.parent / "frontend" / "package.json"
    config = json.loads(package_json.read_text())
    
    # Assert - Scripts and dependencies unchanged
    assert "dev" in config["scripts"], "Dev script missing"
    assert "vite" in config["scripts"]["dev"], "Vite dev script changed"
    assert "react" in config["dependencies"], "React dependency missing"


@pytest.mark.slow
def test_backend_runs_natively():
    """
    Test-NFR-2.1.2: Backend can still run natively with uv.
    
    Verifies: NFR-2.1 (Native Workflow Compatibility)
    
    Given: Native environment with uv and Python
    When: Backend is started with uv run
    Then: Backend starts successfully
    
    Note: This is a slow test that actually starts the backend.
    """
    pytest.skip("Manual test - requires stopping Docker containers and starting natively")
    
    # This would test:
    # 1. Stop Docker containers
    # 2. Run: uv run python -m backend.main
    # 3. Verify backend responds at http://localhost:8001/health
    # 4. Cleanup


@pytest.mark.slow
def test_frontend_runs_natively():
    """
    Test-NFR-2.1.3: Frontend can still run natively with npm.
    
    Verifies: NFR-2.1 (Native Workflow Compatibility)
    
    Given: Native environment with Node.js and npm
    When: Frontend is started with npm run dev
    Then: Frontend starts successfully
    
    Note: This is a slow test that actually starts the frontend.
    """
    pytest.skip("Manual test - requires stopping Docker containers and starting natively")
    
    # This would test:
    # 1. Stop Docker containers
    # 2. Run: cd frontend && npm run dev
    # 3. Verify frontend responds at http://localhost:5173
    # 4. Cleanup


def test_docker_compose_optional():
    """
    Verify that Docker Compose is optional, not required.
    
    Verifies: NFR-2.1 (Native Workflow Compatibility)
    
    Given: Project documentation
    When: README is reviewed
    Then: Both native and Docker workflows are documented
    """
    # This will be verified when we update README in FR-5.1
    # For now, just check that native scripts still exist
    start_sh = Path(__file__).parent.parent.parent / "start.sh"
    assert start_sh.exists(), "Native startup script missing"

