#!/bin/bash
# Setup Skill symlink for a project
# 
# Usage: 
#   cd ~/Code/your-project
#   bash ~/Code/llm-council/setup-skill.sh [skill-name]
#   
# Example:
#   bash ~/Code/llm-council/setup-skill.sh llm-council-dev-process

set -e

PROJECT_DIR=$(pwd)
SKILL_NAME="${1:-vibe-coding}"

# Determine skills location (try Git repo first, fallback to home dir)
if [ -d "/Users/coco/Code/skills" ]; then
    CENTRAL_SKILLS="/Users/coco/Code/skills"
elif [ -d "$HOME/Code/skills" ]; then
    CENTRAL_SKILLS="$HOME/Code/skills"
elif [ -d "$HOME/.skills" ]; then
    CENTRAL_SKILLS="$HOME/.skills"
else
    echo "❌ Error: Skills directory not found"
    echo ""
    echo "Expected locations:"
    echo "  - /Users/coco/Code/skills (Git repository)"
    echo "  - $HOME/Code/skills"
    echo "  - $HOME/.skills"
    echo ""
    echo "💡 To fix this:"
    echo "   1. Clone or create skills repository:"
    echo "      git clone <your-skills-repo> ~/Code/skills"
    echo "   2. Or move Skill to expected location:"
    echo "      mv ~/.skills/$SKILL_NAME ~/Code/skills/"
    echo ""
    exit 1
fi

SKILL_PATH="$CENTRAL_SKILLS/$SKILL_NAME"

echo "🎯 Skill Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Project:       $PROJECT_DIR"
echo "Skill:         $SKILL_NAME"
echo "Skills Repo:   $CENTRAL_SKILLS"
echo "Skill Path:    $SKILL_PATH"
echo ""

# Check if Skill exists
if [ ! -d "$SKILL_PATH" ]; then
    echo "❌ Error: Skill '$SKILL_NAME' not found at $SKILL_PATH"
    echo ""
    echo "Available skills:"
    ls -1 "$CENTRAL_SKILLS" | grep -v "README.md" | grep -v "\.git" || echo "  (none found)"
    echo ""
    echo "💡 To add this Skill:"
    echo "   1. Create the Skill directory:"
    echo "      mkdir -p $SKILL_PATH"
    echo "   2. Add Skill files (instructions.md, metadata.json, etc.)"
    echo ""
    exit 1
fi

# Create .skills directory
echo "📁 Creating .skills directory..."
mkdir -p "$PROJECT_DIR/.skills"

# Check if symlink already exists
if [ -L "$PROJECT_DIR/.skills/$SKILL_NAME" ]; then
    echo "⚠️  Symlink already exists"
    CURRENT_TARGET=$(readlink "$PROJECT_DIR/.skills/$SKILL_NAME")
    if [ "$CURRENT_TARGET" = "$SKILL_PATH" ]; then
        echo "✅ Already pointing to correct location: $CURRENT_TARGET"
    else
        echo "🔄 Updating symlink target..."
        rm "$PROJECT_DIR/.skills/$SKILL_NAME"
        ln -sf "$SKILL_PATH" "$PROJECT_DIR/.skills/"
        echo "✅ Updated to: $SKILL_PATH"
    fi
elif [ -d "$PROJECT_DIR/.skills/$SKILL_NAME" ]; then
    echo "⚠️  Directory exists (not a symlink)"
    echo ""
    read -p "Replace with symlink? This will DELETE the directory. (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$PROJECT_DIR/.skills/$SKILL_NAME"
        ln -sf "$SKILL_PATH" "$PROJECT_DIR/.skills/"
        echo "✅ Replaced with symlink"
    else
        echo "❌ Cancelled. Keeping existing directory."
        exit 1
    fi
else
    echo "🔗 Creating symlink..."
    ln -sf "$SKILL_PATH" "$PROJECT_DIR/.skills/"
    echo "✅ Symlink created"
fi

# Add to .gitignore if not already there
if [ -f "$PROJECT_DIR/.gitignore" ]; then
    if ! grep -q "^\.skills/" "$PROJECT_DIR/.gitignore" 2>/dev/null; then
        echo "" >> "$PROJECT_DIR/.gitignore"
        echo "# Skills (centrally managed via symlinks)" >> "$PROJECT_DIR/.gitignore"
        echo ".skills/" >> "$PROJECT_DIR/.gitignore"
        echo "✅ Added .skills/ to .gitignore"
    else
        echo "✅ .gitignore already configured"
    fi
else
    echo "⚠️  No .gitignore found - creating one"
    echo "# Skills (centrally managed via symlinks)" > "$PROJECT_DIR/.gitignore"
    echo ".skills/" >> "$PROJECT_DIR/.gitignore"
    echo "✅ Created .gitignore with .skills/"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup complete!"
echo ""
echo "📁 Symlink location:"
echo "   $PROJECT_DIR/.skills/$SKILL_NAME"
echo ""
echo "🎯 Points to:"
echo "   $SKILL_PATH"
echo ""
echo "🧪 Test it:"
echo '   Start a conversation with Claude and mention "version" or "FR-1"'
echo ""
echo "📝 To update the Skill (affects all projects):"
echo "   cd $CENTRAL_SKILLS/$SKILL_NAME"
echo "   nano instructions.md"
if [ -d "$CENTRAL_SKILLS/.git" ]; then
    echo "   git commit -am 'Update Skill' && git push"
fi
echo ""
echo "💡 Usage: bash setup-skill.sh [skill-name]"
echo "   Default skill: vibe-coding"
echo "   Example: bash setup-skill.sh vibe-coding"
echo ""

