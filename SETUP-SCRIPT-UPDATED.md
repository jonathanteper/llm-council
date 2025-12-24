# ✅ Setup Script Updated for Skills Git Repository

## What Changed

**`setup-skill.sh`** now points to `/Users/coco/Code/skills` (your Git repository)

### Priority Order:
1. **`/Users/coco/Code/skills`** (Git repo - preferred)
2. **`~/Code/skills`** (alternative location)
3. **`~/.skills`** (fallback for backward compatibility)

## 🚀 Next Steps to Complete Migration

### Step 1: Move Skill to Git Repo

```bash
# Find where your Skill currently is:
ls -la ~/.claude-skills/llm-council-dev-process/ 2>/dev/null && echo "Found in ~/.claude-skills" || \
ls -la ~/.skills/llm-council-dev-process/ 2>/dev/null && echo "Found in ~/.skills" || \
echo "Not found in home directory"

# Move it to Git repo (adjust path based on where you found it):
mv ~/.claude-skills/llm-council-dev-process /Users/coco/Code/skills/
# OR
mv ~/.skills/llm-council-dev-process /Users/coco/Code/skills/
```

### Step 2: Create Symlink in llm-council

```bash
cd /Users/coco/Code/llm-council

# Run the updated setup script
bash setup-skill.sh llm-council-dev-process
```

Expected output:
```
🎯 Skill Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project:       /Users/coco/Code/llm-council
Skill:         llm-council-dev-process
Skills Repo:   /Users/coco/Code/skills
Skill Path:    /Users/coco/Code/skills/llm-council-dev-process

📁 Creating .skills directory...
🔗 Creating symlink...
✅ Symlink created
✅ .gitignore already configured

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Setup complete!
```

### Step 3: Commit to Git

```bash
cd /Users/coco/Code/skills

# Add the Skill
git add llm-council-dev-process/

# Commit
git commit -m "feat: Add LLM Council development process Skill

- Version-based PRD development with FR-X/NFR-X format
- Test-Driven Development (90%+ coverage targets)
- Docker containerization patterns
- Code conventions (Python, JavaScript)
- Git commit standards
- Complete documentation with examples
"

# Push to remote
git push origin main
```

### Step 4: Verify Everything Works

```bash
# Check symlink
ls -la ~/Code/llm-council/.skills/
# Should show: llm-council-dev-process -> /Users/coco/Code/skills/llm-council-dev-process

# Test reading through symlink
cat ~/Code/llm-council/.skills/llm-council-dev-process/metadata.json

# Verify Git tracking
cd /Users/coco/Code/skills
git status
# Should show llm-council-dev-process/ as tracked
```

### Step 5: Clean Up Old Directories (Optional)

```bash
# Remove old home directory locations (if empty)
rmdir ~/.claude-skills 2>/dev/null || echo "Directory not empty or doesn't exist"
rmdir ~/.skills 2>/dev/null || echo "Directory not empty or doesn't exist"
```

## 📊 New Structure

```
/Users/coco/Code/skills/              # Git repository (central)
├── .git/                             # Version controlled
├── README.md                         # Skills inventory
└── llm-council-dev-process/         # Your Skill (master copy)
    ├── INDEX.md
    ├── QUICKSTART.md
    ├── VISUAL-GUIDE.md
    ├── instructions.md               # Core content
    ├── metadata.json                 # Discovery metadata
    └── templates/

/Users/coco/Code/llm-council/
├── .skills/
│   └── llm-council-dev-process/     # Symlink →
│       → /Users/coco/Code/skills/llm-council-dev-process/
└── setup-skill.sh                    # ✅ Updated script
```

## 🎯 Using in Other Projects

Now super easy:

```bash
# In any project
cd ~/Code/your-other-project
bash ~/Code/llm-council/setup-skill.sh

# Or specify a different skill
bash ~/Code/llm-council/setup-skill.sh some-other-skill
```

## 🔄 Updating Skills (New Workflow)

```bash
# 1. Edit the Skill
cd /Users/coco/Code/skills/llm-council-dev-process
nano instructions.md

# 2. Commit and push
cd /Users/coco/Code/skills
git add llm-council-dev-process/
git commit -m "docs: Update TDD workflow"
git push

# 3. All projects automatically see the changes! 🎉
```

## ✅ Features of Updated Script

1. **Flexible Location Detection**
   - Tries `/Users/coco/Code/skills` first (Git repo)
   - Falls back to `~/Code/skills`
   - Falls back to `~/.skills` (backward compatibility)

2. **Skill Name Parameter**
   ```bash
   # Use default skill
   bash setup-skill.sh
   
   # Or specify different skill
   bash setup-skill.sh python-best-practices
   ```

3. **Smart Error Messages**
   - Lists available skills if requested one not found
   - Shows expected locations if skills directory missing
   - Provides helpful recovery instructions

4. **Git Integration**
   - Detects if skills repo is Git-tracked
   - Shows Git commit instructions if applicable

5. **Safety Checks**
   - Won't overwrite existing directory without confirmation
   - Updates symlink if pointing to wrong location
   - Adds `.skills/` to `.gitignore` automatically

## 🎉 Benefits

| Aspect | Old Way | New Way |
|--------|---------|---------|
| **Location** | `~/.claude-skills` | `/Users/coco/Code/skills` |
| **Version Control** | ❌ None | ✅ Full Git history |
| **Backup** | ❌ Manual | ✅ Automatic (GitHub) |
| **Team Sharing** | ❌ Hard | ✅ Easy (`git clone`) |
| **Updates** | Manual copy | `git pull` |
| **Multi-Machine** | Manual sync | `git clone` + `setup-skill.sh` |

## 📝 TODO After Migration

- [ ] Move Skill to `/Users/coco/Code/skills/` (Step 1)
- [ ] Run `bash setup-skill.sh` in llm-council (Step 2)
- [ ] Commit to Git (Step 3)
- [ ] Verify symlink works (Step 4)
- [ ] Update skills README with inventory (Optional)
- [ ] Test with Claude (mention "version" or "FR-1")
- [ ] Clean up old directories (Step 5)

## 🐛 Troubleshooting

### Script says "Skills directory not found"
```bash
# Make sure the skills repo exists
ls -la /Users/coco/Code/skills/

# If not, check where it is
find ~ -name "llm-council-dev-process" -type d 2>/dev/null
```

### Skill not found in skills directory
```bash
# Check what's in the skills repo
ls -la /Users/coco/Code/skills/

# Move Skill if needed
mv <current-location>/llm-council-dev-process /Users/coco/Code/skills/
```

---

**Status:** ✅ Script Updated  
**Ready:** Run migration steps above  
**Script Location:** `~/Code/llm-council/setup-skill.sh`

