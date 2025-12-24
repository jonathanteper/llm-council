#!/bin/bash
# Create symlink to vibe-coding skill in llm-council project

set -e

cd /Users/coco/Code/llm-council

echo "🔗 Setting up vibe-coding skill symlink..."
echo ""

# Create .skills directory if it doesn't exist
mkdir -p .skills

# Remove old symlinks if they exist
rm -rf .skills/llm-council-dev-process 2>/dev/null || true
rm -rf .skills/vibe-coding 2>/dev/null || true

# Create new symlink to vibe-coding
ln -s /Users/coco/Code/skills/vibe-coding .skills/vibe-coding

echo "✅ Symlink created:"
echo "   .skills/vibe-coding -> /Users/coco/Code/skills/vibe-coding"
echo ""

# Verify it works
if [ -f ".skills/vibe-coding/metadata.json" ]; then
    echo "✅ Verification successful - can read metadata.json"
    echo ""
    echo "📋 Skill info:"
    cat .skills/vibe-coding/metadata.json | head -5
else
    echo "⚠️  Warning: Cannot read metadata.json through symlink"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🧪 Test it:"
echo '   Start a conversation with Claude and mention "version" or "FR-1"'
echo ""

