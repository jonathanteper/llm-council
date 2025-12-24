# Renaming .claude-skills to .skills

## ✅ Files Already Updated

The following files have been updated with the new `.skills` naming:

1. ✅ `.gitignore` - Changed to `.skills/`
2. ✅ `setup-claude-skill.sh` → `setup-skill.sh` (content updated)
   - All references changed from `.claude-skills` to `.skills`
   - All references changed from `~/.claude-skills` to `~/.skills`

## 🔄 Manual Steps Required

Due to terminal issues, please run these commands manually:

### Step 1: Rename Central Directory

```bash
mv ~/.claude-skills ~/.skills
```

### Step 2: Update Project Symlink

```bash
cd ~/Code/llm-council

# Remove old directory/symlink
rm -rf .claude-skills

# Create new .skills directory
mkdir -p .skills

# Create new symlink
ln -s ~/.skills/llm-council-dev-process .skills/llm-council-dev-process
```

### Step 3: Rename Setup Script

```bash
cd ~/Code/llm-council
mv setup-claude-skill.sh setup-skill.sh
chmod +x setup-skill.sh
```

### Step 4: Make Rename Script Executable (Optional)

```bash
chmod +x ~/Code/llm-council/rename-to-skills.sh
```

## 🚀 Or Run the Automated Script

I created a script that does all of this:

```bash
cd ~/Code/llm-council
bash rename-to-skills.sh
```

## ✅ Verification

After running the commands, verify:

```bash
# Check central directory
ls -la ~/.skills/
# Should show: llm-council-dev-process/

# Check project symlink  
ls -la ~/Code/llm-council/.skills/
# Should show: llm-council-dev-process -> /Users/coco/.skills/llm-council-dev-process

# Check .gitignore
cat ~/Code/llm-council/.gitignore | grep skills
# Should show: .skills/

# Check setup script exists
ls -l ~/Code/llm-council/setup-skill.sh
# Should exist and be executable
```

## 📋 What Changed

### Before (Claude-specific naming):
```
~/.claude-skills/                    ← Old name
~/Code/project/.claude-skills/       ← Old name
setup-claude-skill.sh                ← Old name
```

### After (Generic naming):
```
~/.skills/                           ← New name
~/Code/project/.skills/              ← New name  
setup-skill.sh                       ← New name
```

## 💡 Why This is Better

- ✅ **Generic** - Not tied to Claude specifically
- ✅ **Flexible** - Can add skills for other AI tools
- ✅ **Cleaner** - Shorter, simpler name
- ✅ **Future-proof** - Works with any AI assistant

## 🎯 Usage in Other Projects

Now use the renamed script:

```bash
cd ~/Code/your-other-project
bash ~/Code/llm-council/setup-skill.sh
```

This will:
1. Create `.skills/` directory
2. Symlink to `~/.skills/llm-council-dev-process`
3. Update `.gitignore` to ignore `.skills/`

---

**Next Step:** Run the commands above or execute `bash rename-to-skills.sh`

