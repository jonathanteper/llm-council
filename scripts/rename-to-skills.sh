#!/bin/bash
# Rename .claude-skills to .skills
# Run this script to complete the renaming

set -e

echo "🔄 Renaming .claude-skills to .skills..."
echo ""

# Step 1: Rename central directory
echo "📁 Step 1: Renaming ~/.claude-skills to ~/.skills"
if [ -d "$HOME/.claude-skills" ]; then
    mv "$HOME/.claude-skills" "$HOME/.skills"
    echo "✅ Central directory renamed"
else
    echo "⚠️  ~/.claude-skills not found (maybe already renamed?)"
fi

# Step 2: Update project symlink
echo ""
echo "🔗 Step 2: Updating symlink in llm-council project"
cd /Users/coco/Code/llm-council

# Remove old .claude-skills directory/symlink
if [ -d ".claude-skills" ] || [ -L ".claude-skills" ]; then
    rm -rf .claude-skills
    echo "✅ Removed old .claude-skills"
fi

# Create new .skills directory
mkdir -p .skills

# Create new symlink
ln -s "$HOME/.skills/llm-council-dev-process" .skills/llm-council-dev-process
echo "✅ Created new symlink: .skills/llm-council-dev-process"

# Step 3: Rename setup script
echo ""
echo "📝 Step 3: Renaming setup script"
if [ -f "setup-claude-skill.sh" ]; then
    mv setup-claude-skill.sh setup-skill.sh
    echo "✅ Renamed to setup-skill.sh"
else
    echo "⚠️  setup-claude-skill.sh not found (maybe already renamed?)"
fi

# Step 4: Verify
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Renaming complete!"
echo ""
echo "📁 Central Skills:"
ls -lh ~/.skills/
echo ""
echo "🔗 Project Symlink:"
ls -la .skills/
echo ""
echo "📝 .gitignore updated to:"
grep "\.skills" .gitignore
echo ""
echo "✅ All references updated from .claude-skills to .skills"
echo ""

