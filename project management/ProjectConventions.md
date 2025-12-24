# Project Conventions: LLM Council

**Version:** 1.1  
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

### Test Organization

```
tests/
├── backend/
│   ├── test_api.py
│   ├── test_council.py
│   └── test_storage.py
└── frontend/
    └── components/
        └── Component.test.jsx
```

### Test Naming

**Python:**
```python
def test_council_processes_query_successfully():
    """Test that council processes a valid query."""
    pass

def test_council_handles_api_error_gracefully():
    """Test error handling when API fails."""
    pass
```

**JavaScript:**
```javascript
describe('Component', () => {
  it('renders with provided title', () => {
    // Test implementation
  });
  
  it('calls onSubmit when button clicked', () => {
    // Test implementation
  });
});
```

### Testing Requirements

- **Unit tests:** Test individual functions/components
- **Integration tests:** Test service interactions
- **E2E tests:** Test full user workflows (if applicable)
- **Coverage goal:** 70%+ for critical paths

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

