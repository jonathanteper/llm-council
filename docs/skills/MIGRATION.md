# Migrating Cursor Dev Skill to Skills Repository

## 🎯 Goal

Move the `llm-council-dev-process` skill from home directory to your skills Git repository at:
- **From:** `~/.skills/llm-council-dev-process/` (or `~/.claude-skills/`)
- **To:** `/Users/coco/Code/skills/llm-council-dev-process/`

Then symlink projects to the Git repository location.

## 📋 Migration Steps

### Step 1: Move Skill to Git Repository

```bash
# Check where the Skill currently is
ls -la ~/.skills/llm-council-dev-process/ 2>/dev/null || \
ls -la ~/.claude-skills/llm-council-dev-process/

# Move to Git repository
# If it's in ~/.skills:
mv ~/.skills/llm-council-dev-process /Users/coco/Code/skills/

# Or if it's still in ~/.claude-skills:
mv ~/.claude-skills/llm-council-dev-process /Users/coco/Code/skills/

# Clean up old directory if empty
rmdir ~/.skills 2>/dev/null || true
rmdir ~/.claude-skills 2>/dev/null || true
```

### Step 2: Verify Skill is in Git Repo

```bash
cd /Users/coco/Code/skills
ls -lh llm-council-dev-process/

# Should show all the Skill files:
# - INDEX.md
# - QUICKSTART.md
# - VISUAL-GUIDE.md
# - INSTALLATION-SUMMARY.md
# - README.md
# - instructions.md
# - metadata.json
# - templates/
```

### Step 3: Update llm-council Project Symlink

```bash
cd /Users/coco/Code/llm-council

# Remove old symlink/directory if exists
rm -rf .skills

# Create new .skills directory
mkdir -p .skills

# Create symlink to Git repo location
ln -s /Users/coco/Code/skills/llm-council-dev-process .skills/llm-council-dev-process

# Verify symlink
ls -la .skills/
# Should show: llm-council-dev-process -> /Users/coco/Code/skills/llm-council-dev-process
```

### Step 4: Update Setup Script

The `setup-skill.sh` needs to point to the new location:

```bash
cd /Users/coco/Code/llm-council
nano setup-skill.sh
```

Change this line:
```bash
CENTRAL_SKILLS="$HOME/.skills"
```

To:
```bash
CENTRAL_SKILLS="/Users/coco/Code/skills"
```

Or make it flexible:
```bash
# Try Git repo first, fallback to home directory
if [ -d "/Users/coco/Code/skills" ]; then
    CENTRAL_SKILLS="/Users/coco/Code/skills"
elif [ -d "$HOME/.skills" ]; then
    CENTRAL_SKILLS="$HOME/.skills"
else
    echo "❌ Error: Skills directory not found"
    exit 1
fi
```

### Step 5: Commit Skill to Git

```bash
cd /Users/coco/Code/skills

# Stage the new Skill
git add llm-council-dev-process/

# Commit
git commit -m "feat: Add LLM Council development process Skill

- Version-based PRD development
- Test-Driven Development (90%+ coverage)
- Docker containerization patterns
- Requirements format (FR-X/NFR-X)
- Code conventions (Python, JavaScript)
- Git commit standards
"

# Push to remote (if you have one)
git push origin main
```

### Step 6: Update Skills Repository README

```bash
cd /Users/coco/Code/skills
nano README.md
```

Add to the README:

```markdown
## 📦 Skills Inventory

### llm-council-dev-process (v1.0)

**Purpose:** Version-based development with TDD, Docker, and documentation standards

**Teaches:**
- Version-based PRD development
- Test-Driven Development (90%+ coverage)
- Docker containerization patterns
- Requirements format (FR-X/NFR-X)
- Code conventions (Python, JavaScript)
- Git commit standards

**Size:** ~8,000 tokens  
**Created:** 2025-12-24  
**Status:** ✅ Active

**Documentation:**
- [INDEX.md](./llm-council-dev-process/INDEX.md)
- [QUICKSTART.md](./llm-council-dev-process/QUICKSTART.md)
- [instructions.md](./llm-council-dev-process/instructions.md)

**Used By:**
- llm-council
```

## 🎯 New Directory Structure

### After Migration:

```
/Users/coco/Code/skills/              # Git repository
├── README.md                         # Skills inventory
└── llm-council-dev-process/         # Your Skill (master copy)
    ├── INDEX.md
    ├── QUICKSTART.md
    ├── VISUAL-GUIDE.md
    ├── INSTALLATION-SUMMARY.md
    ├── README.md
    ├── instructions.md
    ├── metadata.json
    └── templates/

/Users/coco/Code/llm-council/
└── .skills/
    └── llm-council-dev-process/     # Symlink
        → /Users/coco/Code/skills/llm-council-dev-process/
```

## 🚀 Using in Other Projects (Updated)

### For Personal Projects (Local)

```bash
cd ~/Code/your-project
mkdir -p .skills
ln -s /Users/coco/Code/skills/llm-council-dev-process .skills/
echo ".skills/" >> .gitignore
```

### For Team Projects (Share via Git)

Team members clone your skills repo:

```bash
# Team member clones skills repo
git clone git@github.com:yourusername/skills.git ~/Code/skills

# Then links in their projects
cd ~/Code/project-name
mkdir -p .skills
ln -s ~/Code/skills/llm-council-dev-process .skills/
echo ".skills/" >> .gitignore
```

## ✅ Benefits of Git Repo Approach

| Benefit | Description |
|---------|-------------|
| **Version Control** | Full history of Skill changes |
| **Backup** | Automatically backed up on GitHub/GitLab |
| **Team Sharing** | Easy to share via Git clone |
| **Sync Across Machines** | Clone on multiple computers |
| **Pull Requests** | Team can suggest improvements |
| **Release Tags** | Tag versions (v1.0, v1.1) |
| **Documentation** | GitHub README shows Skills inventory |

## 🔄 Updating Skills (With Git)

```bash
# Edit the Skill
cd /Users/coco/Code/skills/llm-council-dev-process
nano instructions.md

# Commit changes
cd /Users/coco/Code/skills
git add llm-council-dev-process/
git commit -m "docs: Update TDD workflow in Skill"
git push

# All projects symlinked to this repo automatically see the changes!
```

## 🤝 Team Workflow

### For You (Skill Author):
```bash
# Make changes
cd /Users/coco/Code/skills/llm-council-dev-process
nano instructions.md

# Commit and push
cd /Users/coco/Code/skills
git commit -am "docs: Update Skill"
git push
```

### For Team Members:
```bash
# Pull latest changes
cd ~/Code/skills
git pull

# Their symlinked projects automatically get the updates!
```

## 📝 Updated Setup Script

Create `/Users/coco/Code/skills/setup-skill.sh`:

```bash
#!/bin/bash
# Setup Skill symlink for a project
# 
# Usage: 
#   cd ~/Code/your-project
#   bash ~/Code/skills/setup-skill.sh llm-council-dev-process

set -e

SKILL_NAME="${1:-llm-council-dev-process}"
PROJECT_DIR=$(pwd)

# Determine skills location
if [ -d "/Users/coco/Code/skills" ]; then
    CENTRAL_SKILLS="/Users/coco/Code/skills"
elif [ -d "$HOME/Code/skills" ]; then
    CENTRAL_SKILLS="$HOME/Code/skills"
elif [ -d "$HOME/.skills" ]; then
    CENTRAL_SKILLS="$HOME/.skills"
else
    echo "❌ Error: Skills directory not found"
    exit 1
fi

SKILL_PATH="$CENTRAL_SKILLS/$SKILL_NAME"

echo "🎯 Skill Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Project:       $PROJECT_DIR"
echo "Skill:         $SKILL_NAME"
echo "Skills Repo:   $CENTRAL_SKILLS"
echo ""

# Check if Skill exists
if [ ! -d "$SKILL_PATH" ]; then
    echo "❌ Error: Skill not found at $SKILL_PATH"
    exit 1
fi

# Create .skills directory
echo "📁 Creating .skills directory..."
mkdir -p "$PROJECT_DIR/.skills"

# Create symlink
echo "🔗 Creating symlink..."
ln -sf "$SKILL_PATH" "$PROJECT_DIR/.skills/"
echo "✅ Symlink created"

# Add to .gitignore
if [ -f "$PROJECT_DIR/.gitignore" ]; then
    if ! grep -q "^\.skills/" "$PROJECT_DIR/.gitignore" 2>/dev/null; then
        echo "" >> "$PROJECT_DIR/.gitignore"
        echo "# Skills (centrally managed via symlinks)" >> "$PROJECT_DIR/.gitignore"
        echo ".skills/" >> "$PROJECT_DIR/.gitignore"
        echo "✅ Added .skills/ to .gitignore"
    else
        echo "✅ .gitignore already configured"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup complete!"
echo ""
echo "📁 Symlink: .skills/$SKILL_NAME"
echo "🎯 Points to: $SKILL_PATH"
echo ""
```

## 🧪 Testing the Migration

```bash
# 1. Verify Skill is in Git repo
ls -la /Users/coco/Code/skills/llm-council-dev-process/

# 2. Verify symlink in llm-council
ls -la /Users/coco/Code/llm-council/.skills/

# 3. Test reading through symlink
cat /Users/coco/Code/llm-council/.skills/llm-council-dev-process/metadata.json

# 4. Verify Git tracking
cd /Users/coco/Code/skills
git status

# 5. Test in Claude
# Start conversation and mention "version" or "FR-1"
```

## 🎉 Summary

**Before:**
- Skill in `~/.skills/` or `~/.claude-skills/`
- Not version controlled
- Hard to share with team

**After:**
- Skill in `/Users/coco/Code/skills/` (Git repo)
- Fully version controlled
- Easy team collaboration via Git
- Backed up on remote

**Next Steps:**
1. Run Step 1-3 to move and symlink
2. Update setup script (Step 4)
3. Commit to Git (Step 5)
4. Update README (Step 6)
5. Test with Claude

---

*Migration Guide*  
*Target: /Users/coco/Code/skills*  
*Approach: Git Repository + Symlinks*

