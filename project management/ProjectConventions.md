# Project Conventions: LLM Council

**Version:** 1.2  
**Date:** December 24, 2025  
**Status:** Active  
**Purpose:** Establish consistent standards and conventions for development

---

## Table of Contents

1. [Requirements Management](#requirements-management)
2. [Documentation Standards](#documentation-standards)
3. [Code Conventions](#code-conventions)
4. [Git Workflow](#git-workflow)
5. [Testing Standards](#testing-standards)
6. [File Organization](#file-organization)

---

## Requirements Management

### Requirement Identification

All requirements must be uniquely identified using a version-qualified format:

**Functional Requirements:**
- Format within PRD: `FR-[number]`
- Format cross-version: `[vX.Y-FR-number]`
- Examples: `FR-1`, `FR-2` (in PRD) or `[v1.1-FR-1]` (in ProductOverview)
- Use for: Features, user-facing functionality, business logic

**Non-Functional Requirements:**
- Format within PRD: `NFR-[number]`
- Format cross-version: `[vX.Y-NFR-number]`
- Examples: `NFR-1`, `NFR-2` (in PRD) or `[v1.1-NFR-1]` (in ProductOverview)
- Use for: Performance, security, scalability, usability, maintainability

**Versioning Rules:**
- Within a version PRD, use short form: `FR-1`, `NFR-1`
- In ProductOverview or cross-version references, use full form: `[v1.1-FR-1]`
- Version numbers follow semantic versioning: `v1.0`, `v1.1`, `v2.0`

### Child Requirements

Requirements can have sub-requirements using dot notation:

**Format:** `FR-[parent].[child]`

**Examples:**
- `FR-1.1` - First sub-requirement of FR-1
- `FR-1.2` - Second sub-requirement of FR-1
- `FR-1.1.1` - Nested sub-requirement

**Usage:**
```markdown
### FR-1: User Authentication

The system shall provide user authentication.

#### FR-1.1: Login Form
The system shall display a login form with username and password fields.

#### FR-1.2: Session Management
The system shall maintain user sessions for 24 hours.

##### FR-1.2.1: Session Timeout
The system shall automatically log out users after 30 minutes of inactivity.
```

### Requirement Priority

Use these priority levels in requirements documents:

- **P0 (Must Have):** Critical for MVP, blocks release if missing
- **P1 (Should Have):** Important but not blocking, defer if needed
- **P2 (Nice to Have):** Desirable, implement if time permits
- **P3 (Future):** Good ideas for later versions

### Requirement Status

Track requirement status using these labels:

- **Draft:** Being written or reviewed
- **Approved:** Accepted and ready for implementation
- **In Progress:** Currently being implemented
- **Implemented:** Code complete, awaiting testing
- **Verified:** Tested and confirmed working
- **Rejected:** Not accepted for implementation
- **Deferred:** Postponed to future release

### Example Requirement Table

**Within a Version PRD:**
```markdown
| ID | Priority | Status | Description | Owner |
|----|----------|--------|-------------|-------|
| FR-1 | P0 | Verified | Backend containerization | DevTeam |
| FR-1.1 | P0 | Verified | Create backend Dockerfile | DevTeam |
| FR-1.2 | P0 | Verified | Configure volume mounts | DevTeam |
| NFR-1 | P1 | In Progress | Hot reload < 2 seconds | DevTeam |
```

**In ProductOverview (cross-version):**
```markdown
| ID | Version | Status | Description | PRD Reference |
|----|---------|--------|-------------|---------------|
| [v1.0-FR-1] | v1.0 | ✅ | Multi-LLM query processing | [PRD](./versions/v1.0/PRD-v1.0.md#fr-1) |
| [v1.1-FR-2] | v1.1 | 🟡 | Docker containerization | [PRD](./versions/v1.1/PRD-v1.1.md#fr-2) |
| [v1.1-FR-2.1] | v1.1 | ⚪ | Backend container | [PRD](./versions/v1.1/PRD-v1.1.md#fr-21) |
| [v2.0-FR-3] | v2.0 | ⚪ | User authentication | [PRD](./versions/v2.0/PRD-v2.0.md#fr-3) |
```

### Requirements Traceability

All PRDs must include a **Requirements Traceability Matrix** that maps User Stories to Requirements.

**Purpose:**
- Ensure all user needs are addressed by requirements
- Identify orphaned requirements (not tied to user value)
- Verify requirements coverage
- Maintain traceability chain: User Need → User Story → Requirements → Implementation → Tests

**Format:**

```markdown
## Requirements Traceability Matrix

| User Story | Functional Requirements | Non-Functional Requirements | Notes |
|------------|------------------------|----------------------------|-------|
| Story 1: Simple Setup | FR-3.1, FR-4.3, FR-5.1 | NFR-4.1 | One-command startup |
| Story 2: Hot Reload | FR-4.1, FR-1.2, FR-2.2, FR-2.3 | NFR-1.2 | Dev experience |
| Story 3: Data Persistence | FR-4.2, FR-1.2 | NFR-3.2 | No data loss |
| Story 4: Cloud Deployment | Out of scope v1.1 | - | Foundation only |
```

**Placement:**
- Add section after "User Stories" and before "Requirements" in PRD
- Update as requirements evolve
- Review during requirement changes to ensure mapping stays current

**Validation:**
- Every user story should map to at least one FR
- Critical user stories should have supporting NFRs
- Requirements without user stories should be justified (technical debt, refactoring, etc.)

---

## Documentation Standards

### Documentation Philosophy

We use a **version-based PRD approach** with **AI-assisted product overview maintenance**:

- **Product Manager (PM)** authors a PRD per version
- **LLMs assist PM** in updating the Product Overview document
- **Product Overview** serves as living architecture and conflict checker
- This approach balances clarity with maintainability

### Document Types & Organization

```
project management/
├── ProjectConventions.md              # This document (how we work)
├── ProductOverview.md                 # Living system documentation
├── versions/
│   ├── v1.0/
│   │   ├── PRD-v1.0.md               # Version 1.0 requirements
│   │   ├── TechnicalSpec-v1.0.md     # Version 1.0 architecture
│   │   └── ReleaseNotes-v1.0.md      # What shipped in v1.0
│   ├── v1.1/
│   │   ├── PRD-v1.1.md               # Version 1.1 requirements
│   │   ├── TechnicalSpec-v1.1.md     # Version 1.1 architecture
│   │   ├── ImplementationPlan-v1.1.md # How to implement v1.1
│   │   └── ReleaseNotes-v1.1.md      # What shipped in v1.1 (when done)
│   └── v2.0/
│       └── PRD-v2.0.md               # Next version (draft)
└── archives/
    └── [deprecated documents]
```

**Key Documents:**

- **ProductOverview.md** - Living document that describes:
  - All product capabilities (referencing version PRDs)
  - Technical architecture (updated per version)
  - Feature dependencies and conflicts
  - Technology stack evolution
  - Updated by PM with LLM assistance

- **PRD-vX.Y.md** - Version-scoped product requirements:
  - Created by PM for each version
  - Contains functional and non-functional requirements
  - Clear scope boundaries per release
  - Archived after version ships

- **TechnicalSpec-vX.Y.md** - Version-scoped technical specifications:
  - Detailed architecture for the version
  - Container specs, APIs, data models
  - Implementation details

- **ImplementationPlan-vX.Y.md** - Version-scoped implementation guide:
  - Step-by-step implementation instructions
  - Testing checklists
  - Rollback strategies

- **ReleaseNotes-vX.Y.md** - What actually shipped:
  - Created when version is released
  - Documents what was implemented vs planned
  - Known issues and workarounds

### Version-Based Requirement References

When referencing requirements across documents, use version-qualified IDs:

**Format:** `[vX.Y-FR-N]` or `[vX.Y-NFR-N]`

**Examples:**
- `[v1.0-FR-1]` - Core query processing from v1.0
- `[v1.1-FR-2]` - Docker containerization from v1.1
- `[v1.1-FR-2.1]` - Backend containerization (child of FR-2)
- `[v2.0-NFR-5]` - Performance requirement from v2.0

**Within a version PRD:** Use short form `FR-1` (version is implied)

**In ProductOverview or cross-version references:** Use full form `[v1.0-FR-1]`

### Product Overview Maintenance Workflow

The PM uses LLMs to keep ProductOverview.md current with minimal effort:

**When Creating New Version PRD:**

1. **PM writes** `PRD-vX.Y.md` with new requirements
2. **PM prompts LLM:**
   ```
   I've created PRD-v1.2.md (attached). Please update ProductOverview.md:
   
   1. Add new capabilities section for v1.2 features
   2. Check for conflicts with existing features (list key ones)
   3. Update technical architecture section if needed
   4. Update technology stack table
   5. Update version history and roadmap
   
   Provide the updated sections for ProductOverview.md.
   ```

3. **PM reviews** LLM suggestions and edits as needed
4. **PM commits** both PRD and updated ProductOverview

**LLM-Assisted Conflict Checking:**

Use this prompt when adding features:

```
Review PRD-vX.Y.md against ProductOverview.md and check for conflicts:

1. Port number conflicts
2. Data model changes affecting backward compatibility
3. API changes impacting existing features
4. Environment variable conflicts
5. Resource constraints (CPU, memory, storage)

For each conflict found, specify:
- Severity: High/Medium/Low
- Affected feature: [version-FR-ID]
- Recommended resolution

Also note: What dependencies does this version have on previous versions?
```

**LLM-Assisted Architecture Updates:**

```
Based on PRD-vX.Y.md, update the Technical Architecture section:

1. Add any new technologies to the stack table
2. Update system architecture if data flows changed
3. Note any new external dependencies
4. Update architecture diagram (Mermaid) if needed

Provide updated content for ProductOverview.md architecture section.
```

### Benefits of This Approach

✅ **Clear scope per version** - Each PRD is focused and time-boxed
✅ **System-level view** - ProductOverview prevents siloed thinking
✅ **Conflict detection** - LLM helps spot integration issues early
✅ **Low maintenance** - LLMs reduce PM overhead significantly
✅ **Easy onboarding** - New team members read ProductOverview + relevant PRD
✅ **Clean archives** - Old version docs stay intact and readable

### Document Structure

All major documents should include:

```markdown
# Document Title

**Version:** X.Y
**Date:** YYYY-MM-DD
**Status:** Draft|Active|Deprecated
**Author/Owner:** Name or Team

---

## Table of Contents
(Auto-generated or manual list)

## Sections
(Content organized logically)

## Appendix
(References, glossary, related docs)
```

### Markdown Conventions

**Headers:**
- Use `#` for document title
- Use `##` for major sections
- Use `###` for subsections
- Maximum depth: `####` (4 levels)

**Code Blocks:**
- Always specify language: ` ```python`, ` ```bash`, ` ```javascript`
- Include comments for clarity
- Keep examples concise and runnable

**Links:**
- Use relative paths for internal docs: `[PRD](./PRD.md)`
- Use absolute paths for external: `[GitHub](https://github.com/...)`
- Link to related documents in Appendix

**Emphasis:**
- Use **bold** for important terms and UI elements
- Use *italics* for emphasis
- Use `code` for file names, commands, variables

**Diagrams:**
- Use Mermaid for architecture diagrams
- Keep diagrams simple and focused
- Include text description for accessibility

### Version Control

- Document version format: `Major.Minor`
- Increment Minor for small updates
- Increment Major for significant rewrites
- Update "Last Updated" date with each change

---

## Code Conventions

### Python (Backend)

**File Organization:**
```
backend/
├── __init__.py
├── main.py           # FastAPI application entry point
├── config.py         # Configuration and environment variables
├── models.py         # Data models (if needed)
├── routes/           # API route handlers (if split)
└── utils/            # Utility functions
```

**Naming:**
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case()`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`

**Style:**
- Follow PEP 8
- Maximum line length: 100 characters
- Use type hints where practical
- Docstrings for public functions

**Example:**
```python
"""Module for council orchestration."""

from typing import List, Dict

DEFAULT_TIMEOUT = 30  # seconds

class CouncilOrchestrator:
    """Orchestrates LLM council interactions."""
    
    def __init__(self, models: List[str]) -> None:
        """Initialize orchestrator with model list."""
        self.models = models
    
    async def process_query(self, query: str) -> Dict:
        """Process a query through the council."""
        # Implementation
        pass
```

### JavaScript/React (Frontend)

**File Organization:**
```
frontend/src/
├── components/       # React components
│   ├── Component.jsx
│   └── Component.css
├── api.js           # API client
├── App.jsx          # Main app component
└── main.jsx         # Entry point
```

**Naming:**
- Files: `PascalCase.jsx` for components, `camelCase.js` for utilities
- Components: `PascalCase`
- Functions: `camelCase()`
- Constants: `UPPER_SNAKE_CASE`
- CSS classes: `kebab-case`

**Style:**
- Use functional components with hooks
- Props destructuring in parameters
- Named exports for utilities, default for components

**Example:**
```javascript
// Component.jsx
import React, { useState, useEffect } from 'react';
import './Component.css';

export default function Component({ title, onSubmit }) {
  const [value, setValue] = useState('');
  
  const handleSubmit = () => {
    onSubmit(value);
  };
  
  return (
    <div className="component-container">
      <h2>{title}</h2>
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}
```

### Configuration Files

**Environment Variables (.env):**
```bash
# API Keys
OPENROUTER_API_KEY=sk-or-v1-...

# Configuration
DEBUG=false
LOG_LEVEL=info
```

**Comments:**
- Group related variables
- Document expected format/values
- Never commit sensitive values

---

## Git Workflow

### Branch Strategy

**Main Branches:**
- `master` - Production-ready code
- `develop` - Integration branch (if needed for larger team)

**Feature Branches:**
- Format: `feature/short-description`
- Example: `feature/docker-setup`
- Create from: `master`
- Merge to: `master` (via PR for review)

**Hotfix Branches:**
- Format: `hotfix/issue-description`
- Example: `hotfix/api-key-loading`
- Create from: `master`
- Merge to: `master` immediately

### Commit Messages

**Format:**
```
[Type] Brief description (50 chars or less)

More detailed explanation if needed (wrap at 72 characters).
Include motivation for change and how it differs from previous behavior.

- Bullet points for multiple changes
- Keep commits focused and atomic

Related: FR-1, NFR-3
```

**Types:**
- `feat:` - New feature (FR implementation)
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, no logic change)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Build process, dependencies, tooling

**Examples:**
```
feat: Add Docker Compose configuration

- Create docker-compose.yml with backend and frontend services
- Configure volume mounts for hot reload
- Add health checks for service dependencies

Implements: [v1.1-FR-1], [v1.1-FR-1.3]
```

```
fix: Resolve .env file loading in containers

Backend was not finding .env file due to incorrect working directory.
Mount .env as read-only volume at /app/.env.

Fixes: #42
Related: [v1.1-FR-1.2]
```

### Commit Best Practices

- **Atomic commits:** One logical change per commit
- **Working code:** Each commit should build and pass tests
- **Clear messages:** Explain what and why, not just how
- **Reference requirements:** Link commits to version-qualified IDs like `[v1.1-FR-1]`
- **Tag versions:** Use git tags for releases: `git tag v1.1.0`

---

## Testing Standards

### Testing Philosophy

We follow **Strict Test-Driven Development (TDD)** with **advisory enforcement**:

- **High Standards:** Write tests before code, aim for 90%+ coverage
- **Self-Discipline:** Tests inform but don't block commits (team accountability)
- **Testability First:** Design for testability from the requirement phase
- **Progressive Rigor:** More tests as features mature and become critical

**Core Principle:** Tests are living documentation that prove the system works as designed.

### Test-Driven Development Workflow

**Standard TDD Cycle (Red → Green → Refactor):**

1. **Write Test First** (Red)
   - Read the requirement (FR-X.Y)
   - Write test that validates the requirement
   - Test fails (no implementation yet)

2. **Write Minimal Code** (Green)
   - Implement just enough to make test pass
   - Test passes

3. **Refactor** (Clean)
   - Improve code quality
   - Tests still pass
   - Commit

**Example Flow:**
```bash
# 1. Write test for FR-1.1 (Backend Dockerfile)
$ touch tests/backend/test_dockerfile.py
$ # Write test_backend_image_builds()
$ pytest tests/backend/test_dockerfile.py  # FAILS ❌

# 2. Create Dockerfile
$ touch backend.Dockerfile
$ # Write minimal Dockerfile
$ pytest tests/backend/test_dockerfile.py  # PASSES ✅

# 3. Refactor and commit
$ git add backend.Dockerfile tests/backend/test_dockerfile.py
$ git commit -m "feat: Add backend Dockerfile (FR-1.1)"
```

### Testability Requirements

**Every FR must be independently testable:**

When writing requirements, ask:
- ✅ "How will I verify this works?"
- ✅ "Can I test this in isolation?"
- ✅ "What are the inputs and expected outputs?"

**Bad (not testable):**
```markdown
FR-1: The system shall be fast
```

**Good (testable):**
```markdown
FR-1: Hot Reload Performance

The system shall reload code changes within 2 seconds.

**Test Acceptance Criteria:**
- Test-1.1: Modify Python file → reload completes < 2s
- Test-1.2: Modify React file → HMR completes < 2s
- Test-1.3: Measure 10 reloads → 90th percentile < 2s

**Test Type:** Integration
**Risk Level:** Medium
```

### Requirement Test Planning

All FRs and NFRs must include:

```markdown
#### FR-X.Y: Requirement Title

The system shall...

**Test Plan:**
- Test-X.Y.1: [Specific test case]
- Test-X.Y.2: [Specific test case]
- Test-X.Y.3: [Specific test case]

**Test Type:** Unit | Integration | E2E
**Risk Level:** High | Medium | Low
**Coverage Target:** 90% | 70% | 50%
**Test Files:** `tests/backend/test_feature.py`
**Status:** ⏳ 2/3 passing | ✅ 3/3 passing
```

### Coverage Targets

**Strict Coverage Standards:**

| Code Type | Target | Rationale |
|-----------|--------|-----------|
| **Core Features** (v1.0 code still used) | 90%+ | Critical path, high risk |
| **New Features** (current version) | 90%+ | Build quality in from start |
| **Utilities/Helpers** | 95%+ | Reused everywhere, must be solid |
| **UI Components** | 70%+ | Visual testing harder to automate |
| **Overall Project** | 90%+ | Maintain high standard across codebase |

**Measuring Coverage:**

```bash
# Backend
pytest --cov=backend --cov-report=term-missing --cov-fail-under=90

# Frontend
npm test -- --coverage --coverageThreshold='{"global":{"lines":90}}'
```

### Test Organization

**Directory Structure:**

```
tests/
├── backend/
│   ├── unit/
│   │   ├── test_config.py
│   │   ├── test_council.py
│   │   └── test_storage.py
│   ├── integration/
│   │   ├── test_api_endpoints.py
│   │   └── test_openrouter_integration.py
│   └── e2e/
│       └── test_council_workflow.py
├── frontend/
│   ├── unit/
│   │   └── components/
│   │       ├── ChatInterface.test.jsx
│   │       └── Sidebar.test.jsx
│   ├── integration/
│   │   └── test_api_client.test.js
│   └── e2e/
│       └── test_user_flows.test.js
└── conftest.py  # Shared fixtures
```

### Test Naming Conventions

**Python (pytest):**
```python
def test_council_processes_query_successfully():
    """Test FR-1.1: Council processes valid query through all stages."""
    # Arrange
    council = CouncilOrchestrator(models=TEST_MODELS)
    query = "What is quantum computing?"
    
    # Act
    result = await council.process_query(query)
    
    # Assert
    assert result.stage1_responses is not None
    assert len(result.stage1_responses) == len(TEST_MODELS)
    assert result.stage3_synthesis is not None

def test_council_handles_api_error_gracefully():
    """Test NFR-2.1: System handles OpenRouter API errors."""
    # Arrange
    council = CouncilOrchestrator(models=["invalid/model"])
    
    # Act & Assert
    with pytest.raises(APIError) as exc_info:
        await council.process_query("test")
    assert "OpenRouter error" in str(exc_info.value)
```

**JavaScript (Jest/Vitest):**
```javascript
describe('ChatInterface (FR-4.1)', () => {
  it('should render query input and submit button', () => {
    // Arrange
    render(<ChatInterface />);
    
    // Act
    const input = screen.getByPlaceholderText('Ask your question...');
    const button = screen.getByRole('button', { name: /submit/i });
    
    // Assert
    expect(input).toBeInTheDocument();
    expect(button).toBeInTheDocument();
  });
  
  it('should call onSubmit when form submitted (FR-4.1.1)', () => {
    // Arrange
    const mockOnSubmit = jest.fn();
    render(<ChatInterface onSubmit={mockOnSubmit} />);
    
    // Act
    const input = screen.getByPlaceholderText('Ask your question...');
    fireEvent.change(input, { target: { value: 'test query' } });
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    // Assert
    expect(mockOnSubmit).toHaveBeenCalledWith('test query');
  });
});
```

### Test Types

**Unit Tests:**
- Test individual functions/classes in isolation
- Mock all external dependencies
- Fast execution (milliseconds)
- 90%+ coverage target

**Integration Tests:**
- Test multiple components working together
- May use real external services (or test doubles)
- Moderate execution time (seconds)
- Cover critical paths

**End-to-End Tests:**
- Test complete user workflows
- Use real browser, real services
- Slow execution (minutes)
- Cover major user stories

### Definition of Done

A requirement is "Done" when:

**For All Requirements:**
1. ✅ Tests written BEFORE code (TDD)
2. ✅ All tests passing
3. ✅ Code implemented
4. ✅ Coverage target met (90%+ for most code)
5. ✅ Code reviewed
6. ✅ Documentation updated

**Additional for HIGH Risk:**
7. ✅ Integration tests included
8. ✅ Added to regression test suite

### Test Enforcement Policy

**Advisory, Not Blocking:**
- ❌ Tests do NOT block commits
- ❌ Tests do NOT block merges
- ❌ Tests do NOT block releases
- ✅ Tests inform the team
- ✅ Team holds each other accountable
- ✅ Coverage reports visible in PRs

**Rationale:** Trust and discipline over automation. The team commits to TDD as a practice, not because tools force it.

**Visibility:**
```bash
# Run before commit (but doesn't block)
$ pytest --cov=backend --cov-report=term
$ npm test -- --coverage

# Show in PR description
Coverage: 92% (+2% from main)
Tests: 156 passing, 0 failing
```

### Regression Testing

**Between Versions:** TBD - will evolve as project scales

**Initial Approach:**
- Run full test suite before version releases
- Document any breaking changes
- Manual smoke testing of critical paths

**Future Considerations:**
- Automated regression matrix across versions
- Snapshot testing for UI consistency
- Performance regression tracking

### Test Data Management

**Fixtures and Mocks:**
```python
# tests/conftest.py
import pytest

@pytest.fixture
def mock_openrouter_response():
    """Mock OpenRouter API response for testing."""
    return {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "Test response from GPT"
            }
        }]
    }

@pytest.fixture
def test_conversation():
    """Sample conversation for testing."""
    return {
        "id": "test-123",
        "messages": [
            {"role": "user", "content": "What is AI?"}
        ]
    }
```

### Continuous Improvement

**Test Metrics to Track:**
- Coverage percentage over time
- Test execution time
- Flaky test rate
- Bug escape rate (bugs found in production vs caught by tests)

**Review Questions:**
- Are tests catching bugs before production?
- Is TDD making code design better?
- Are tests documentation-quality?
- Is coverage meaningful or just high numbers?

---

## File Organization

### Directory Structure

```
llm-council/
├── backend/                         # Python backend code
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── [feature].py
├── frontend/                        # React frontend code
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── data/                            # Persistent data (gitignored)
│   └── conversations/
├── project management/              # Documentation
│   ├── ProjectConventions.md       # This document
│   ├── ProductOverview.md          # Living system doc (all versions)
│   ├── versions/
│   │   ├── v1.0/
│   │   │   ├── PRD-v1.0.md
│   │   │   ├── TechnicalSpec-v1.0.md
│   │   │   └── ReleaseNotes-v1.0.md
│   │   ├── v1.1/
│   │   │   ├── PRD-v1.1.md
│   │   │   ├── TechnicalSpec-v1.1.md
│   │   │   ├── ImplementationPlan-v1.1.md
│   │   │   └── ReleaseNotes-v1.1.md
│   │   └── v2.0/
│   │       └── PRD-v2.0.md
│   └── archives/                    # Deprecated documents
├── utilities/                       # Development utilities
│   └── [helper_scripts].py
├── tests/                           # Test files (if created)
├── .env                             # Environment variables (gitignored)
├── .gitignore
├── README.md                        # User-facing documentation
├── pyproject.toml                   # Python dependencies
└── start.sh                         # Development startup script
```

### File Naming

**General Rules:**
- Use descriptive names
- Avoid abbreviations unless well-known
- Keep names concise but clear

**Examples:**
- ✅ `CouncilOrchestrator.py`, `council_orchestrator.py`
- ✅ `ChatInterface.jsx`, `api.js`
- ❌ `co.py`, `ci.jsx`, `utils.js`

### What to .gitignore

```gitignore
# Environment
.env
.env.*

# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/

# Data
data/

# Build artifacts
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

---

## Change Log

### Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.2 | 2025-12-24 | Add strict TDD standards, test-first workflow, 90%+ coverage targets, testability requirements, advisory enforcement policy | Development Team |
| 1.1 | 2025-12-24 | Add version-based PRD workflow, LLM-assisted ProductOverview maintenance, version-qualified requirement IDs | Development Team |
| 1.0 | 2025-12-24 | Initial version with requirements format, documentation standards, code conventions | Development Team |

---

## Related Documents

- [Product Overview](./ProductOverview.md) - Living system documentation
- [Version PRDs](./versions/) - Version-specific requirements
- [Main README](../README.md) - User-facing documentation

---

**Document Status:** Active  
**Last Updated:** December 24, 2025  
**Next Review:** As needed when new conventions are required

