# Vibe Coding Skill - Setup Guide

## 📍 Skill Location

**GitHub:** https://github.com/jonathanteper/skills/tree/main/vibe-coding  
**Local:** `/Users/coco/Code/skills/vibe-coding`

This is the "LLM Council Development Process" skill, now named **vibe-coding** in your skills repository.

## 🔗 Quick Setup

### For llm-council Project

```bash
cd /Users/coco/Code/llm-council

# Run the quick setup script
bash link-vibe-coding-skill.sh

# Or use the general setup script
bash setup-skill.sh vibe-coding
```

### For Other Projects

```bash
cd ~/Code/your-other-project

# Option 1: Use setup script from llm-council
bash ~/Code/llm-council/setup-skill.sh vibe-coding

# Option 2: Manual setup
mkdir -p .skills
ln -s /Users/coco/Code/skills/vibe-coding .skills/vibe-coding
echo ".skills/" >> .gitignore
```

## 📊 Current Setup

```
GitHub Repository:
https://github.com/jonathanteper/skills
├── README.md
└── vibe-coding/                      ← Your Skill (master copy)
    ├── instructions.md
    ├── metadata.json
    └── ... (all Skill files)

Local (Synced with Git):
/Users/coco/Code/skills/
└── vibe-coding/                      ← Same as GitHub

llm-council Project:
/Users/coco/Code/llm-council/
└── .skills/
    └── vibe-coding/                  ← Symlink
        → /Users/coco/Code/skills/vibe-coding/
```

## 🎯 What the Skill Teaches

**Vibe Coding Skill** (formerly "LLM Council Development Process"):
- Version-based PRD development
- Test-Driven Development (90%+ coverage)
- Docker containerization patterns
- Requirements format (FR-X/NFR-X)
- Code conventions (Python, JavaScript)
- Git commit standards

## 🔄 Updating the Skill

Since it's in a Git repository:

```bash
# 1. Edit the Skill
cd /Users/coco/Code/skills/vibe-coding
nano instructions.md

# 2. Commit changes
cd /Users/coco/Code/skills
git add vibe-coding/
git commit -m "docs: Update vibe-coding skill"

# 3. Push to GitHub
git push origin main

# 4. All projects symlinked to it automatically see the changes!
```

## 🤝 Team Usage

### For Team Members

**Step 1:** Clone the skills repository
```bash
git clone https://github.com/jonathanteper/skills.git ~/Code/skills
```

**Step 2:** Link in their projects
```bash
cd ~/Code/their-project
mkdir -p .skills
ln -s ~/Code/skills/vibe-coding .skills/vibe-coding
echo ".skills/" >> .gitignore
```

**Step 3:** Keep updated
```bash
cd ~/Code/skills
git pull
# Their projects automatically get the updates!
```

## 🧪 Verification

Check if symlink is working:

```bash
# In llm-council project
ls -la /Users/coco/Code/llm-council/.skills/
# Should show: vibe-coding -> /Users/coco/Code/skills/vibe-coding

# Test reading through symlink
cat /Users/coco/Code/llm-council/.skills/vibe-coding/metadata.json

# Test with Claude
# Start a conversation and mention "version" or "FR-1"
# Claude should automatically load and apply the skill
```

## 📝 Files Reference

| File | Purpose |
|------|---------|
| `link-vibe-coding-skill.sh` | Quick setup for llm-council |
| `setup-skill.sh` | General setup (default: vibe-coding) |
| `.gitignore` | Ignores `.skills/` directory |
| `.skills/vibe-coding/` | Symlink to skill (not committed) |

## 🎓 Using the Skill

Once linked, Claude will automatically discover and use the skill when you:
- Mention "**version**" (v1.2, v2.0, etc.)
- Reference "**FR-**" or "**NFR-**" (requirements)
- Discuss "**test**" or "**TDD**"
- Talk about "**docker**" or "**containerization**"
- Create "**PRD**" or "**documentation**"

Claude will apply your development standards automatically! 🎉

## 🔗 Quick Links

- **GitHub Repository:** https://github.com/jonathanteper/skills
- **Skill Directory:** https://github.com/jonathanteper/skills/tree/main/vibe-coding
- **Local Path:** `/Users/coco/Code/skills/vibe-coding`
- **Documentation:** See `vibe-coding/INDEX.md` for navigation

---

**Skill Name:** vibe-coding  
**Repository:** jonathanteper/skills  
**Type:** Development Process Skill  
**Status:** ✅ Active

