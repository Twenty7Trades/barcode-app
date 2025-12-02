# Notes Agent - Quick Start (Global Installation)

## 🚀 Install Once, Use Everywhere

### Step 1: Install Globally

```bash
cd "/Applications/LLM-Generator1.0 2/notes-agent"
./install-notes-agent-global.sh
```

### Step 2: Add to PATH (if needed)

```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"

# Reload
source ~/.zshrc
```

### Step 3: Use in Any Project

```bash
# Navigate to any project
cd ~/projects/my-project

# Initialize (one time per project)
notes-agent init

# Add session summary
notes-agent session --json '{"title":"My Session","summary":"What I did","decisions":["Decision"],"files":["file.py"],"blockers":[],"nextSteps":["Next"]}'

# View summary
notes-agent summary
```

## 🤖 AI Assistant Integration

When you work with an AI assistant (like me), just say:

> **"Generate session summary"** or **"Save today's session"**

I'll automatically:
1. Detect the current project
2. Analyze our conversation
3. Extract key information
4. Generate a session entry
5. Save it to the project's SESSION_LOG.md

**No manual input needed!**

## 📋 What Gets Created

Each project will have:
- `notes-agent/config.json` - Project-specific configuration
- `PROJECT_NOTES.md` - Main project documentation
- `SESSION_LOG.md` - Work session summaries
- `DEPLOYMENT_LOG.md` - Deployment history

## ✅ Verify Installation

```bash
# Check if installed
which notes-agent

# Should output: /Users/YOUR_USERNAME/.local/bin/notes-agent

# Test in any directory
notes-agent summary
```

## 🎯 Benefits

✅ **One installation** - Install once, use everywhere  
✅ **Auto-detection** - Finds project root automatically  
✅ **AI-friendly** - Works seamlessly with AI assistants  
✅ **Project-specific** - Each project has its own config/logs  
✅ **No copying** - Global tool, local configs  

**Ready to use!** Install it once and use it in all your projects! 🚀


