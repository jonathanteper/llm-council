# Central Claude Skills Setup

This project uses a **centrally managed Claude Skill** stored in `~/.claude-skills/`.

## 📁 Structure

```
~/.claude-skills/                           # Central storage
└── llm-council-dev-process/               # The actual Skill
    ├── instructions.md
    ├── metadata.json
    └── ... (all Skill files)

~/Code/llm-council/.claude-skills/          # This project
└── llm-council-dev-process -> ~/.claude-skills/llm-council-dev-process/  # Symlink

~/Code/other-project/.claude-skills/        # Another project
└── llm-council-dev-process -> ~/.claude-skills/llm-council-dev-process/  # Same symlink
```

## ✅ Benefits

- **Single Source of Truth** - Update once, benefits all projects
- **Version Control** - Skills directory can be its own Git repo
- **Easy Maintenance** - One place to maintain conventions
- **Portable** - Link from any project instantly
- **No Duplication** - Skill content exists only once

## 🚀 Using This Skill in Other Projects

### For New Projects

```bash
# 1. Create .claude-skills directory
cd ~/Code/your-other-project
mkdir -p .claude-skills

# 2. Create symlink to central Skill
ln -s ~/.claude-skills/llm-council-dev-process .claude-skills/

# 3. Verify
ls -la .claude-skills/
# Should show: llm-council-dev-process -> /Users/coco/.claude-skills/llm-council-dev-process

# 4. Add to .gitignore (symlink should not be committed in other projects)
echo ".claude-skills/" >> .gitignore
```

### For Existing Projects

Same as above - just create the symlink in each project's `.claude-skills/` directory.

## 🔄 Updating the Skill

Since the Skill is centrally stored, updates automatically apply to all projects:

```bash
# Edit the central Skill
nano ~/.claude-skills/llm-council-dev-process/instructions.md

# Update version
nano ~/.claude-skills/llm-council-dev-process/metadata.json
# Change "version": "1.0" to "1.1"

# All projects now use the updated Skill!
```

## 📦 Version Controlling the Skills (Optional)

You can make `~/.claude-skills/` its own Git repository:

```bash
cd ~/.claude-skills/
git init
git add llm-council-dev-process/
git commit -m "feat: Add LLM Council development process Skill"

# Optional: Push to GitHub for backup/sharing
git remote add origin git@github.com:yourusername/claude-skills.git
git push -u origin main
```

## 🤝 Sharing with Team

### Option 1: Central Skills Repository (Recommended)

```bash
# Team member clones the Skills repo
git clone git@github.com:yourusername/claude-skills.git ~/.claude-skills

# Then creates symlink in each project
cd ~/Code/llm-council
mkdir -p .claude-skills
ln -s ~/.claude-skills/llm-council-dev-process .claude-skills/
```

### Option 2: Project-Specific (Original Approach)

If you want some projects to have the Skill in version control:

```bash
# Remove symlink
rm .claude-skills/llm-council-dev-process

# Copy the Skill
cp -r ~/.claude-skills/llm-council-dev-process .claude-skills/

# Commit to repo
git add .claude-skills/
git commit -m "feat: Add Claude Skill to project"
```

## 🎯 Current Setup (llm-council)

This project currently uses the **symlink approach**:

```bash
# The symlink
.claude-skills/llm-council-dev-process -> ~/.claude-skills/llm-council-dev-process/

# Symlink is in .gitignore (not committed)
# Actual Skill is in ~/.claude-skills/ (centrally managed)
```

## 📋 Setup Script for Other Projects

Save this as `setup-claude-skill.sh`:

```bash
#!/bin/bash
# Setup Claude Skill symlink for a project

PROJECT_DIR=$(pwd)
SKILL_NAME="llm-council-dev-process"
CENTRAL_SKILLS="$HOME/.claude-skills"
SKILL_PATH="$CENTRAL_SKILLS/$SKILL_NAME"

# Check if central Skill exists
if [ ! -d "$SKILL_PATH" ]; then
    echo "❌ Error: Skill not found at $SKILL_PATH"
    echo "💡 Run this in llm-council first to create the central Skill"
    exit 1
fi

# Create .claude-skills directory
mkdir -p "$PROJECT_DIR/.claude-skills"

# Create symlink
ln -sf "$SKILL_PATH" "$PROJECT_DIR/.claude-skills/"

# Add to .gitignore if not already there
if ! grep -q "^\.claude-skills/" "$PROJECT_DIR/.gitignore" 2>/dev/null; then
    echo ".claude-skills/" >> "$PROJECT_DIR/.gitignore"
    echo "✅ Added .claude-skills/ to .gitignore"
fi

echo "✅ Claude Skill linked successfully!"
echo "📁 Symlink: .claude-skills/$SKILL_NAME -> $SKILL_PATH"
```

Usage:
```bash
# In any project
cd ~/Code/your-project
bash ~/Code/llm-council/setup-claude-skill.sh
```

## 🔍 Verifying the Setup

```bash
# Check if symlink exists and points to the right place
ls -la .claude-skills/

# Read the Skill metadata through the symlink
cat .claude-skills/llm-council-dev-process/metadata.json

# Verify Claude can see it (test in conversation)
# Mention "version" or "FR-1" and see if Claude loads the Skill
```

## 🐛 Troubleshooting

### Symlink Broken?
```bash
# Remove and recreate
rm .claude-skills/llm-council-dev-process
ln -s ~/.claude-skills/llm-council-dev-process .claude-skills/
```

### Want to Stop Using Central Skill?
```bash
# Replace symlink with actual copy
rm .claude-skills/llm-council-dev-process
cp -r ~/.claude-skills/llm-council-dev-process .claude-skills/
```

### Want to Use Different Skill Per Project?
Just don't create the symlink - copy the Skill and modify per project.

## 📊 Comparison: Symlink vs Copy

| Aspect | Symlink (Central) | Copy (Per-Project) |
|--------|-------------------|-------------------|
| **Maintenance** | Update once | Update each project |
| **Consistency** | Always same | Can diverge |
| **Version Control** | Separate repo | In project repo |
| **Team Sharing** | Separate clone | Automatic with project |
| **Customization** | Same for all | Can customize per project |
| **Storage** | One copy | Multiple copies |

**Recommendation:** Use symlink for personal development, copy for team projects with project-specific needs.

## ✅ Current Status

- ✅ Skill moved to `~/.claude-skills/llm-council-dev-process/`
- ✅ Symlink created in this project
- ✅ `.gitignore` updated (symlink not committed)
- ✅ Ready to link from other projects

---

**Next Steps:**
1. Use `ln -s ~/.claude-skills/llm-council-dev-process .claude-skills/` in other projects
2. Consider version controlling `~/.claude-skills/` as a Git repo
3. Share Skills repo with team if needed

---

*Setup Date: December 24, 2025*  
*Structure: Central Skills with Symlinks*  
*Benefits: Single source of truth, easy updates*

