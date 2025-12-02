# Notes Agent System

## 🎯 Purpose
The **Notes Agent** is a universal session documentation system that works across all Cursor projects. It prevents information loss by automatically tracking:
- Session summaries
- Key decisions and why they were made
- Files changed and why
- Technical debt created
- Next steps and blockers

## 🚀 Installation

### Step 1: Install Globally (One Time)

```bash
cd /Applications/CursorRules/notes-agent-system
./install-notes-agent-global.sh
```

This installs the `notes-agent` command globally at `~/.local/bin/notes-agent`.

### Step 2: Add to PATH (If Needed)

If the script warns about PATH, add this to your `~/.zshrc`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload:

```bash
source ~/.zshrc
```

### Step 3: Verify Installation

```bash
which notes-agent
# Should output: /Users/YOUR_USERNAME/.local/bin/notes-agent
```

## 📦 Deploy to Projects

Use the CursorRules deploy script to add notes-agent to any project:

```bash
cd /Applications/CursorRules
./deploy-notes-agent.sh /Applications/Mockup-Image-Creator
./deploy-notes-agent.sh /Applications/Fit-Comments
./deploy-notes-agent.sh /Applications/SEO-AI
./deploy-notes-agent.sh /Applications/barcode-app
```

This copies the notes-agent directory and initializes it in each project.

## 🤖 AI Assistant Commands

Once deployed, the AI assistant in any project will recognize these commands:

- **"take a session summary"**
- **"save session summary"**
- **"document this session"**
- **"create session entry"**
- **"save this session"**
- **"save work"**
- **"document work"**

The AI will automatically:
1. Analyze the conversation
2. Extract key information (what was done, decisions, files changed)
3. Generate a structured session entry
4. Save it to `SESSION_LOG.md`

## 📋 Manual Usage

### Initialize in a New Project

```bash
cd /Applications/YourProject
notes-agent init
```

### Add a Session Summary

```bash
notes-agent session --json '{
  "title": "2025-11-15 - Fixed Authentication Bug",
  "summary": "Fixed TypeError in dashboard route when user session expires",
  "decisions": [
    "Enhanced login_required decorator to verify user exists in database",
    "Added safety check in dashboard route"
  ],
  "files": ["app.py"],
  "blockers": [],
  "nextSteps": ["Test session expiry flow", "Add unit tests"]
}'
```

### View Project Summary

```bash
notes-agent summary
```

## 📁 Files Created

Each project will have:

- **`notes-agent/`** - Notes agent system directory
  - `config.json` - Project-specific configuration
  - `notes-agent.js` - Core Node.js implementation
  - `notes_agent_mcp.py` - Python wrapper for CLI
  - `generate_session.py` - Session generator helper

- **`PROJECT_NOTES.md`** - Main project documentation
  - Critical information
  - Live URLs
  - Key configurations
  - Important decisions & fixes
  - Troubleshooting log

- **`SESSION_LOG.md`** - Work session summaries
  - Date and title
  - What was accomplished
  - Key decisions
  - Files changed
  - Blockers and next steps

- **`DEPLOYMENT_LOG.md`** - Deployment history
  - Deployment dates
  - Changes deployed
  - Status and notes

## 🎯 How It Works

### Global Installation
- `install-notes-agent-global.sh` copies all notes-agent files to `~/.local/share/notes-agent/`
- Creates a wrapper script at `~/.local/bin/notes-agent`
- The wrapper is globally accessible from any directory

### Project-Specific Configuration
- Each project has its own `notes-agent/` directory
- Contains `config.json` with project-specific settings
- Local notes-agent tools read from this config

### AI Integration
- `.cursorrules` file tells the AI about session summary keywords
- AI recognizes commands like "save session summary"
- AI extracts information from the conversation
- AI formats it as JSON and calls `notes-agent session --json '{...}'`
- Session is saved to `SESSION_LOG.md`

## 🔧 Troubleshooting

### "notes-agent: command not found"

```bash
# Check if ~/.local/bin is in PATH
echo $PATH | grep ".local/bin"

# If not found, add to ~/.zshrc:
export PATH="$HOME/.local/bin:$PATH"
source ~/.zshrc
```

### "Project not initialized"

```bash
# Run init in the project directory
cd /Applications/YourProject
notes-agent init
```

### Node.js Required

Notes agent uses Node.js. Verify it's installed:

```bash
node --version
# Should show v14+ or higher
```

## 📚 Related Systems

This notes-agent system works alongside:
- **Information Preservation System** (backups, time-based versioning)
- **`.cursorrules`** (AI behavior rules)
- **Agent Task System** (for autonomous work tracking)

## 🎓 Best Practices

1. **Save sessions frequently** - Don't lose work if chat resets
2. **Document decisions** - Future you will thank present you
3. **Include WHY, not just WHAT** - Context is critical
4. **List all files changed** - Makes it easy to find relevant code
5. **Track next steps** - Pick up where you left off

## 🚀 Quick Start Example

```bash
# Install globally (one time)
cd /Applications/CursorRules/notes-agent-system
./install-notes-agent-global.sh

# Deploy to a project
cd /Applications/YourProject
notes-agent init

# In Cursor chat, just say:
# "Take a session summary"

# The AI handles everything else!
```

## ✅ Verification

Test that it's working:

```bash
# 1. Check global installation
which notes-agent

# 2. Go to a project
cd /Applications/YourProject

# 3. Check if initialized
ls notes-agent/config.json

# 4. View summary
notes-agent summary

# 5. In Cursor chat, say:
# "Take a session summary"
```

---

**You're all set!** Install once, use everywhere, never lose important information again. 🎉

