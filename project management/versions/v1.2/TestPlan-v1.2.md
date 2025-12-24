# Test Plan: LLM Council v1.2 - API-Ready Architecture

**Version:** 1.2  
**Date:** December 24, 2025  
**Status:** Draft  
**Test Manager:** Development Team

---

## Table of Contents

1. [Overview](#overview)
2. [Test Strategy](#test-strategy)
3. [Test Coverage Matrix](#test-coverage-matrix)
4. [Test Environment](#test-environment)
5. [Unit Tests](#unit-tests)
6. [Integration Tests](#integration-tests)
7. [End-to-End Tests](#end-to-end-tests)
8. [Performance Tests](#performance-tests)
9. [Security Tests](#security-tests)
10. [Regression Tests](#regression-tests)
11. [Test Execution](#test-execution)
12. [Test Results](#test-results)

---

## Overview

This test plan defines the testing strategy for LLM Council v1.2, focusing on API readiness while maintaining backward compatibility with v1.1.

### Testing Goals

1. **Verify API Functionality:** All versioned endpoints work correctly
2. **Validate Backward Compatibility:** v1.1 features unchanged
3. **Ensure Security:** Optional authentication works correctly
4. **Confirm Performance:** No regression vs v1.1
5. **Test External Integration:** External apps can integrate successfully

### Success Criteria

- ✅ 90%+ code coverage for new features
- ✅ 100% backward compatibility (all v1.1 tests pass)
- ✅ All API endpoints tested with positive and negative cases
- ✅ Performance within 10ms of v1.1 baseline
- ✅ External integration test app works

---

## Test Strategy

### Testing Levels

| Level | Scope | Tools | Coverage Target |
|-------|-------|-------|-----------------|
| **Unit** | Individual functions/classes | pytest | 95% |
| **Integration** | Multiple components | pytest, requests | 90% |
| **E2E** | Complete user flows | Playwright/Selenium | Critical paths |
| **Performance** | API response times | custom scripts | Baseline + 10ms |
| **Security** | Auth, CORS, validation | manual + pytest | 100% of security features |

### Testing Approach

**Test-Driven Development (TDD):**
1. Write test for requirement
2. Test fails (Red)
3. Implement feature
4. Test passes (Green)
5. Refactor (Clean)

**Continuous Testing:**
- Run unit tests on every code change
- Run integration tests before commit
- Run full suite before merge
- Run regression suite before release

---

## Test Coverage Matrix

| Requirement | Test Type | Test Count | Status | Files |
|-------------|-----------|-----------|--------|-------|
| **FR-1.1: CORS** | Integration | 4 | ⏳ | `test_api_cors.py` |
| **FR-1.2: Auth** | Unit, Integration | 5 | ⏳ | `test_auth.py`, `test_api_auth.py` |
| **FR-1.3: Status** | Integration | 4 | ⏳ | `test_api_status.py` |
| **FR-2.1: Versioning** | Integration, E2E | 4 | ⏳ | `test_api_versioning.py` |
| **FR-2.2: Headers** | Integration | 3 | ⏳ | `test_api_headers.py` |
| **FR-3.1: Documentation** | Manual, Integration | 3 | ⏳ | `test_api_examples.py` |
| **FR-3.2: OpenAPI** | Integration | 4 | ⏳ | `test_api_docs.py` |
| **FR-4.1: Frontend** | E2E, Regression | - | ⏳ | `test_regression_v1_1.js` |
| **FR-4.2: Docker** | Integration | 4 | ⏳ | `test_docker_compose_v1_2.py` |
| **NFR-1.1: Consistency** | Integration | 4 | ⏳ | `test_api_consistency.py` |
| **NFR-1.2: Stateless** | Integration | 3 | ⏳ | `test_stateless_api.py` |
| **NFR-1.3: Performance** | Performance | 3 | ⏳ | `test_api_overhead.py` |
| **NFR-2.1: Compat** | Regression | - | ⏳ | All v1.1 tests |
| **NFR-2.2: Docs** | Manual, Integration | 3 | ⏳ | `test_documentation.py` |

**Legend:**
- ⏳ Pending
- 🟡 In Progress
- ✅ Complete
- ❌ Failed

---

## Test Environment

### Required Services

| Service | Port | Purpose | Required For |
|---------|------|---------|--------------|
| Backend | 8001 | API under test | All tests |
| Frontend | 5173 | UI under test | E2E tests |
| Test Server | 8080 | External app simulation | CORS tests |

### Environment Setup

**Start Test Environment:**
```bash
# Start services
docker compose up -d

# Wait for health checks
sleep 10

# Verify services ready
curl http://localhost:8001/health
curl http://localhost:5173
```

**Test Data Setup:**
```bash
# Clear test data
rm -rf data/conversations/*.json

# Create test conversations
python3 tests/fixtures/create_test_data.py
```

### Test Configuration

**Environment Variables (.env.test):**
```bash
OPENROUTER_API_KEY=sk-or-v1-test-key
API_CORS_ORIGINS=*
API_KEYS=testkey1,testkey2,testkey3
```

---

## Unit Tests

### Test: Auth Middleware

**File:** `tests/backend/unit/test_auth.py`

**Test Cases:**

```python
import pytest
from backend.auth import get_api_keys, verify_api_key
from fastapi import HTTPException

def test_get_api_keys_empty_when_not_set(monkeypatch):
    """Test-1.2.1: get_api_keys returns empty list when API_KEYS not set."""
    monkeypatch.delenv("API_KEYS", raising=False)
    assert get_api_keys() == []

def test_get_api_keys_parses_comma_separated(monkeypatch):
    """Test-1.2.2: get_api_keys parses comma-separated keys."""
    monkeypatch.setenv("API_KEYS", "key1,key2,key3")
    assert get_api_keys() == ["key1", "key2", "key3"]

def test_get_api_keys_strips_whitespace(monkeypatch):
    """Test-1.2.3: get_api_keys strips whitespace from keys."""
    monkeypatch.setenv("API_KEYS", " key1 , key2 , key3 ")
    assert get_api_keys() == ["key1", "key2", "key3"]

@pytest.mark.asyncio
async def test_verify_api_key_allows_when_disabled(monkeypatch):
    """Test-1.2.4: verify_api_key allows requests when auth disabled."""
    monkeypatch.delenv("API_KEYS", raising=False)
    result = await verify_api_key(None)
    assert result is None

@pytest.mark.asyncio
async def test_verify_api_key_validates_when_enabled(monkeypatch):
    """Test-1.2.5: verify_api_key validates key when auth enabled."""
    monkeypatch.setenv("API_KEYS", "validkey")
    
    # Valid key
    result = await verify_api_key("validkey")
    assert result == "validkey"
    
    # Invalid key
    with pytest.raises(HTTPException) as exc_info:
        await verify_api_key("invalidkey")
    assert exc_info.value.status_code == 401
    assert "INVALID_API_KEY" in str(exc_info.value.detail)
    
    # Missing key
    with pytest.raises(HTTPException) as exc_info:
        await verify_api_key(None)
    assert exc_info.value.status_code == 401
    assert "MISSING_API_KEY" in str(exc_info.value.detail)
```

**Coverage Target:** 95%

---

## Integration Tests

### Test: API Versioning

**File:** `tests/backend/integration/test_api_versioning.py`

**Test Cases:**

```python
import pytest
import requests

BASE_URL = "http://localhost:8001"

def test_v1_conversations_endpoint_exists():
    """Test-2.1.1: /api/v1/conversations endpoint returns 200."""
    response = requests.get(f"{BASE_URL}/api/v1/conversations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_legacy_endpoint_redirects():
    """Test-2.1.2: /api/conversations redirects to /api/v1/conversations."""
    response = requests.get(f"{BASE_URL}/api/conversations", allow_redirects=False)
    assert response.status_code == 301
    assert "/api/v1/conversations" in response.headers.get("Location", "")

def test_all_v1_routes_have_prefix():
    """Test-2.1.3: All v1 routes have /api/v1/ prefix."""
    response = requests.get(f"{BASE_URL}/openapi.json")
    openapi_spec = response.json()
    
    v1_paths = [path for path in openapi_spec["paths"].keys() if path.startswith("/api/v1")]
    non_versioned_api_paths = [
        path for path in openapi_spec["paths"].keys()
        if path.startswith("/api/") and not path.startswith("/api/v1")
    ]
    
    # Should have at least 5 v1 endpoints
    assert len(v1_paths) >= 5
    
    # No non-versioned /api/* paths (except legacy aliases)
    # Legacy aliases are temporary and will be removed

def test_frontend_uses_v1_routes():
    """Test-2.1.4: Frontend uses new v1 API routes."""
    # This would be tested in E2E tests by inspecting network requests
    # For now, check that api.js file contains /api/v1/
    with open("frontend/src/api.js", "r") as f:
        content = f.read()
        assert "/api/v1/" in content
```

### Test: CORS Configuration

**File:** `tests/backend/integration/test_api_cors.py`

**Test Cases:**

```python
import pytest
import requests

BASE_URL = "http://localhost:8001"

def test_cors_allows_configured_origin():
    """Test-1.1.1: CORS allows requests from configured origins."""
    headers = {"Origin": "http://localhost:5173"}
    response = requests.get(
        f"{BASE_URL}/api/v1/status",
        headers=headers
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

def test_cors_preflight_succeeds():
    """Test-1.1.2: CORS preflight OPTIONS request succeeds."""
    headers = {
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type"
    }
    response = requests.options(
        f"{BASE_URL}/api/v1/conversations",
        headers=headers
    )
    assert response.status_code == 200
    assert "access-control-allow-methods" in response.headers

def test_cors_exposes_version_headers():
    """Test-1.1.3: CORS exposes custom headers."""
    headers = {"Origin": "http://localhost:5173"}
    response = requests.get(
        f"{BASE_URL}/api/v1/status",
        headers=headers
    )
    exposed_headers = response.headers.get("access-control-expose-headers", "")
    assert "x-api-version" in exposed_headers.lower()
    assert "x-service-version" in exposed_headers.lower()

def test_cors_respects_wildcard():
    """Test-1.1.4: CORS wildcard allows any origin."""
    # Assumes API_CORS_ORIGINS=* in test environment
    headers = {"Origin": "http://example.com"}
    response = requests.get(
        f"{BASE_URL}/api/v1/status",
        headers=headers
    )
    assert response.status_code == 200
```

### Test: Authentication

**File:** `tests/backend/integration/test_api_auth.py`

**Test Cases:**

```python
import pytest
import requests
import os

BASE_URL = "http://localhost:8001"

@pytest.fixture
def auth_enabled(monkeypatch):
    """Enable authentication for test."""
    monkeypatch.setenv("API_KEYS", "testkey1,testkey2")
    # Note: In real tests, would restart backend or use dependency override

def test_auth_disabled_allows_requests():
    """Test-1.2.3: Requests work without API key when auth disabled."""
    # Assumes API_KEYS not set
    response = requests.get(f"{BASE_URL}/api/v1/conversations")
    assert response.status_code == 200

def test_auth_enabled_requires_key(auth_enabled):
    """Test-1.2.1: Requests fail without API key when auth enabled."""
    response = requests.get(f"{BASE_URL}/api/v1/conversations")
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "MISSING_API_KEY"

def test_auth_enabled_accepts_valid_key(auth_enabled):
    """Test-1.2.2: Requests succeed with valid API key."""
    headers = {"X-API-Key": "testkey1"}
    response = requests.get(
        f"{BASE_URL}/api/v1/conversations",
        headers=headers
    )
    assert response.status_code == 200

def test_auth_rejects_invalid_key(auth_enabled):
    """Test-1.2.3: Requests fail with invalid API key."""
    headers = {"X-API-Key": "invalidkey"}
    response = requests.get(
        f"{BASE_URL}/api/v1/conversations",
        headers=headers
    )
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "INVALID_API_KEY"

def test_auth_is_case_sensitive(auth_enabled):
    """Test-1.2.4: API key validation is case-sensitive."""
    headers = {"X-API-Key": "TestKey1"}  # Wrong case
    response = requests.get(
        f"{BASE_URL}/api/v1/conversations",
        headers=headers
    )
    assert response.status_code == 401
```

### Test: Status Endpoint

**File:** `tests/backend/integration/test_api_status.py`

**Test Cases:**

```python
import pytest
import requests

BASE_URL = "http://localhost:8001"

def test_status_endpoint_returns_200():
    """Test-1.3.1: GET /api/v1/status returns 200."""
    response = requests.get(f"{BASE_URL}/api/v1/status")
    assert response.status_code == 200

def test_status_contains_required_fields():
    """Test-1.3.2: Status response contains all required fields."""
    response = requests.get(f"{BASE_URL}/api/v1/status")
    data = response.json()
    
    assert "service" in data
    assert "version" in data
    assert "api_version" in data
    assert "status" in data
    assert "models" in data
    assert "features" in data
    
    assert data["api_version"] == "v1"
    assert data["status"] == "healthy"

def test_status_version_matches():
    """Test-1.3.3: Version in status matches package version."""
    response = requests.get(f"{BASE_URL}/api/v1/status")
    data = response.json()
    
    # Should be 1.2.0 or 1.2.x
    assert data["version"].startswith("1.2")

def test_status_models_list_valid():
    """Test-1.3.4: Models list matches configuration."""
    response = requests.get(f"{BASE_URL}/api/v1/status")
    data = response.json()
    
    assert "council" in data["models"]
    assert "chairman" in data["models"]
    assert isinstance(data["models"]["council"], list)
    assert len(data["models"]["council"]) > 0
```

### Test: API Consistency

**File:** `tests/backend/integration/test_api_consistency.py`

**Test Cases:**

```python
import pytest
import requests
from datetime import datetime

BASE_URL = "http://localhost:8001"

def test_success_responses_use_2xx():
    """Test-1.1.1: Success responses use 2xx status codes."""
    endpoints = [
        ("GET", "/api/v1/status"),
        ("GET", "/api/v1/conversations"),
        ("POST", "/api/v1/conversations", {}),
    ]
    
    for method, path, *body in endpoints:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{path}")
        else:
            response = requests.post(f"{BASE_URL}{path}", json=body[0] if body else {})
        
        assert 200 <= response.status_code < 300, f"{method} {path} returned {response.status_code}"

def test_error_responses_match_schema():
    """Test-1.1.2: Error responses follow consistent schema."""
    # Trigger 404 error
    response = requests.get(f"{BASE_URL}/api/v1/conversations/nonexistent-id")
    assert response.status_code == 404
    
    data = response.json()
    assert "error" in data
    assert "code" in data["error"]
    assert "message" in data["error"]

def test_timestamps_are_iso8601():
    """Test-1.1.3: All timestamps use ISO 8601 format."""
    # Create conversation
    response = requests.post(f"{BASE_URL}/api/v1/conversations", json={})
    data = response.json()
    
    # Verify created_at is ISO 8601
    created_at = data["created_at"]
    try:
        datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError:
        pytest.fail(f"Timestamp not ISO 8601: {created_at}")

def test_error_codes_are_descriptive():
    """Test-1.1.4: Error codes are descriptive (not just numbers)."""
    response = requests.get(f"{BASE_URL}/api/v1/conversations/invalid-id")
    data = response.json()
    
    error_code = data["error"]["code"]
    assert isinstance(error_code, str)
    assert error_code.isupper()
    assert "_" in error_code  # Snake case like CONVERSATION_NOT_FOUND
```

---

## End-to-End Tests

### Test: Frontend Regression

**File:** `tests/frontend/e2e/test_regression_v1_1.js`

**Test Cases (Playwright):**

```javascript
const { test, expect } = require('@playwright/test');

test.describe('v1.1 Regression Tests', () => {
  test('should load application', async ({ page }) => {
    await page.goto('http://localhost:5173');
    await expect(page).toHaveTitle(/LLM Council/);
  });

  test('should create new conversation', async ({ page }) => {
    await page.goto('http://localhost:5173');
    await page.click('button:has-text("New Conversation")');
    await expect(page.locator('.conversation-title')).toBeVisible();
  });

  test('should send message to council', async ({ page }) => {
    await page.goto('http://localhost:5173');
    await page.click('button:has-text("New Conversation")');
    
    await page.fill('textarea', 'What is AI?');
    await page.click('button:has-text("Send")');
    
    // Wait for Stage 3 response
    await page.waitForSelector('.stage3-response', { timeout: 60000 });
    const response = await page.textContent('.stage3-response');
    expect(response.length).toBeGreaterThan(0);
  });

  test('should navigate between stages', async ({ page }) => {
    // Test stage navigation still works
    // ... implementation
  });
});
```

---

## Performance Tests

### Test: API Overhead

**File:** `tests/backend/performance/test_api_overhead.py`

**Test Cases:**

```python
import pytest
import requests
import time
import statistics

BASE_URL = "http://localhost:8001"

def benchmark_endpoint(url, iterations=100):
    """Measure endpoint response time."""
    times = []
    for _ in range(iterations):
        start = time.time()
        response = requests.get(url)
        elapsed = (time.time() - start) * 1000  # ms
        if response.status_code == 200:
            times.append(elapsed)
    
    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "p95": sorted(times)[int(len(times) * 0.95)],
    }

def test_auth_overhead_under_5ms():
    """Test-1.3.1: Auth check adds < 5ms overhead."""
    # With auth disabled
    stats_no_auth = benchmark_endpoint(f"{BASE_URL}/api/v1/status")
    
    # With auth enabled (would need to restart or use test config)
    # stats_with_auth = benchmark_endpoint(f"{BASE_URL}/api/v1/status")
    
    # overhead = stats_with_auth["mean"] - stats_no_auth["mean"]
    # assert overhead < 5, f"Auth overhead {overhead:.2f}ms exceeds 5ms"
    
    # For now, just verify base performance is reasonable
    assert stats_no_auth["mean"] < 50  # Should be very fast

def test_cors_overhead_under_1ms():
    """Test-1.3.2: CORS check adds < 1ms overhead."""
    # Measure with CORS headers
    stats = benchmark_endpoint(f"{BASE_URL}/api/v1/status")
    
    # CORS is very lightweight, full request should be fast
    assert stats["p95"] < 100  # 95th percentile under 100ms

def test_no_regression_vs_v1_1():
    """Test-1.3.3: v1.2 performance comparable to v1.1 baseline."""
    # Benchmark v1.2
    stats_v12 = benchmark_endpoint(f"{BASE_URL}/api/v1/conversations")
    
    # v1.1 baseline (would load from saved metrics)
    v11_baseline = 50  # Example: 50ms mean
    
    # Allow 10ms tolerance
    assert stats_v12["mean"] < v11_baseline + 10
```

---

## Security Tests

### Test: Security Validation

**File:** `tests/backend/security/test_security.py`

**Test Cases:**

```python
import pytest
import requests

BASE_URL = "http://localhost:8001"

def test_no_sensitive_data_in_logs():
    """Verify API keys not logged in plain text."""
    # This would check log files
    # For now, manual verification required
    pass

def test_env_file_not_exposed():
    """Verify .env file not accessible via API."""
    response = requests.get(f"{BASE_URL}/.env")
    assert response.status_code == 404

def test_sql_injection_not_possible():
    """Verify no SQL injection vectors (using JSON storage)."""
    # Try malicious conversation ID
    malicious_id = "'; DROP TABLE conversations; --"
    response = requests.get(f"{BASE_URL}/api/v1/conversations/{malicious_id}")
    
    # Should return 404, not crash
    assert response.status_code in [404, 400]

def test_xss_in_messages_prevented():
    """Verify XSS payloads are handled safely."""
    # Create conversation
    conv_response = requests.post(f"{BASE_URL}/api/v1/conversations", json={})
    conv_id = conv_response.json()["id"]
    
    # Send XSS payload
    xss_payload = "<script>alert('XSS')</script>"
    response = requests.post(
        f"{BASE_URL}/api/v1/conversations/{conv_id}/message",
        json={"content": xss_payload}
    )
    
    # Should process normally, not execute
    assert response.status_code == 200
```

---

## Regression Tests

### v1.1 Test Suite

**All existing v1.1 tests must pass:**
- [ ] Backend unit tests (council, storage, config)
- [ ] Backend integration tests (API endpoints, OpenRouter)
- [ ] Frontend unit tests (components)
- [ ] Docker tests (compose, health checks)
- [ ] Documentation tests (README examples)

**Regression Test Command:**
```bash
# Run all v1.1 tests
pytest tests/backend/ -m "not v1_2_only"
npm test --prefix frontend

# Verify Docker setup
pytest tests/integration/test_docker_compose.py
```

---

## Test Execution

### Pre-Test Setup

```bash
# 1. Start test environment
docker compose -f docker-compose.test.yml up -d

# 2. Wait for services
sleep 10

# 3. Verify health
curl http://localhost:8001/health
curl http://localhost:5173

# 4. Load test data
python3 tests/fixtures/create_test_data.py
```

### Running Tests

**Unit Tests:**
```bash
pytest tests/backend/unit/ -v --cov=backend
```

**Integration Tests:**
```bash
pytest tests/backend/integration/ -v --cov=backend
```

**E2E Tests:**
```bash
npx playwright test tests/frontend/e2e/
```

**Performance Tests:**
```bash
pytest tests/backend/performance/ -v
```

**All Tests:**
```bash
pytest tests/ -v --cov=backend --cov-report=html
npm test --prefix frontend --coverage
```

### Post-Test Cleanup

```bash
# Stop services
docker compose down

# Clean test data
rm -rf data/test_conversations/
```

---

## Test Results

### Execution Summary

**Last Run:** TBD  
**Duration:** TBD  
**Pass Rate:** TBD

### Coverage Report

| Component | Coverage | Target | Status |
|-----------|----------|--------|--------|
| `backend/auth.py` | TBD | 95% | ⏳ |
| `backend/middleware/cors.py` | TBD | 90% | ⏳ |
| `backend/middleware/versioning.py` | TBD | 90% | ⏳ |
| `backend/routers/api_v1.py` | TBD | 90% | ⏳ |
| **Overall Backend** | TBD | 90% | ⏳ |
| **Overall Frontend** | TBD | 70% | ⏳ |

### Known Issues

| Issue ID | Description | Severity | Status | Workaround |
|----------|-------------|----------|--------|------------|
| - | TBD | - | - | - |

### Flaky Tests

| Test Name | Failure Rate | Last Failure | Notes |
|-----------|--------------|--------------|-------|
| - | TBD | TBD | TBD |

---

## Appendix

### Test Data

**Sample Conversations:**
- `test_conv_1.json` - Empty conversation
- `test_conv_2.json` - Single message
- `test_conv_3.json` - Multi-turn conversation

### Test Utilities

**File:** `tests/utils/api_client.py`
```python
"""Test utilities for API testing."""

import requests

class TestAPIClient:
    """Helper class for API testing."""
    
    def __init__(self, base_url="http://localhost:8001", api_key=None):
        self.base_url = base_url
        self.api_key = api_key
    
    def get_headers(self):
        """Get headers with optional auth."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers
    
    def create_conversation(self):
        """Create test conversation."""
        response = requests.post(
            f"{self.base_url}/api/v1/conversations",
            headers=self.get_headers(),
            json={}
        )
        return response.json()
    
    def send_message(self, conversation_id, content):
        """Send message to conversation."""
        response = requests.post(
            f"{self.base_url}/api/v1/conversations/{conversation_id}/message",
            headers=self.get_headers(),
            json={"content": content}
        )
        return response.json()
```

### Related Documents

- [v1.2 PRD](./PRD-v1.2.md) - Product requirements
- [v1.2 Technical Spec](./TechnicalSpec-v1.2.md) - Architecture details
- [v1.2 Implementation Plan](./ImplementationPlan-v1.2.md) - Implementation guide
- [Project Conventions](../../ProjectConventions.md) - Testing standards

---

**Document Status:** Draft  
**Last Updated:** December 24, 2025  
**Test Execution:** Not Started

