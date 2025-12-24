#!/bin/bash
# Complete root directory cleanup
# Run this script to finish the reorganization

set -e

cd /Users/coco/Code/llm-council

echo "🧹 Completing root directory cleanup..."
echo ""

# Step 1: Create directories
echo "📁 Creating directories..."
mkdir -p docs/skills scripts

# Step 2: Move documentation files
echo "📄 Moving documentation..."
if [ -f "CLAUDE.md" ]; then
    mv CLAUDE.md docs/
    echo "  ✓ Moved CLAUDE.md → docs/"
fi

if [ -f "README_API.md" ]; then
    mv README_API.md docs/API.md
    echo "  ✓ Moved README_API.md → docs/API.md"
fi

if [ -f "VIBE-CODING-SKILL-SETUP.md" ]; then
    mv VIBE-CODING-SKILL-SETUP.md docs/skills/SETUP.md
    echo "  ✓ Moved VIBE-CODING-SKILL-SETUP.md → docs/skills/SETUP.md"
fi

if [ -f "MIGRATE-TO-SKILLS-REPO.md" ]; then
    mv MIGRATE-TO-SKILLS-REPO.md docs/skills/MIGRATION.md
    echo "  ✓ Moved MIGRATE-TO-SKILLS-REPO.md → docs/skills/MIGRATION.md"
fi

# Step 3: Move scripts
echo ""
echo "🔧 Moving scripts..."
if [ -f "start.sh" ]; then
    mv start.sh scripts/
    echo "  ✓ Moved start.sh → scripts/"
fi

if [ -f "setup-skill.sh" ]; then
    mv setup-skill.sh scripts/
    echo "  ✓ Moved setup-skill.sh → scripts/"
fi

if [ -f "link-vibe-coding-skill.sh" ]; then
    mv link-vibe-coding-skill.sh scripts/
    echo "  ✓ Moved link-vibe-coding-skill.sh → scripts/"
fi

if [ -f "rename-to-skills.sh" ]; then
    mv rename-to-skills.sh scripts/
    echo "  ✓ Moved rename-to-skills.sh → scripts/"
fi

# Step 4: Delete temporary files
echo ""
echo "🗑️  Deleting temporary files..."
rm -f setup-claude-skill.sh && echo "  ✓ Deleted setup-claude-skill.sh" || echo "  - setup-claude-skill.sh not found"
rm -f RENAME-INSTRUCTIONS.md && echo "  ✓ Deleted RENAME-INSTRUCTIONS.md" || echo "  - RENAME-INSTRUCTIONS.md not found"
rm -f SETUP-SCRIPT-UPDATED.md && echo "  ✓ Deleted SETUP-SCRIPT-UPDATED.md" || echo "  - SETUP-SCRIPT-UPDATED.md not found"
rm -f commit-and-push.sh && echo "  ✓ Deleted commit-and-push.sh" || echo "  - commit-and-push.sh not found"
rm -f COMMIT_MESSAGE.txt && echo "  ✓ Deleted COMMIT_MESSAGE.txt" || echo "  - COMMIT_MESSAGE.txt not found"

# Step 5: Check for duplicate main.py
if [ -f "main.py" ]; then
    if [ -f "backend/main.py" ]; then
        rm -f main.py
        echo "  ✓ Deleted duplicate main.py"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Cleanup complete!"
echo ""
echo "📊 Final structure:"
echo ""
echo "Root directory:"
ls -1 | grep -v -E "^(backend|frontend|tests|utilities|docs|scripts|project|data|node_modules|__pycache__|\.)" | head -20
echo ""
echo "docs/ directory:"
ls -1 docs/
echo ""
echo "scripts/ directory:"
ls -1 scripts/
echo ""
echo "Next: Review changes and commit"
echo "  git status"
echo "  git add -A"
echo "  git commit -m 'refactor: Reorganize root directory structure'"
echo ""

