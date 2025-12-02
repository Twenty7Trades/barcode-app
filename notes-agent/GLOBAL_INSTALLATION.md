# Notes Agent - Global Installation Guide (MCP/CLI)

Transform your notes-agent into a **globally accessible tool** that works from any project without copying files!

## 🚀 Quick Install (Global CLI)

### Option 1: Automated Install Script

```bash
cd "/Applications/LLM-Generator1.0 2/notes-agent"
./install-notes-agent-global.sh
```

This will:
- Install notes-agent to `~/.local/share/notes-agent`
- Create a global `notes-agent` command in `~/.local/bin`
- Make it accessible from any project directory

### Option 2: Manual Installation

```bash
# 1. Copy to global location
mkdir -p ~/.local/share/notes-agent
cp -r "/Applications/LLM-Generator1.0 2/notes-agent"/* ~/.local/share/notes-agent/

# 2. Create global command
mkdir -p ~/.local/bin
cat > ~/.local/bin/notes-agent << 'EOF'
#!/bin/bash
python3 ~/.local/share/notes-agent/notes_agent_mcp.py "$@"
EOF
chmod +x ~/.local/bin/notes-agent

# 3. Add to PATH (if not already there)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## 📋 Usage (Global CLI)

Once installed, you can use `notes-agent` from **any project directory**:

```bash
# Initialize notes-agent in current project
notes-agent init

# Add a session (JSON input)
notes-agent session --json '{"title":"My Session","summary":"What I did","decisions":["Decision 1"],"files":["file1.py"],"blockers":[],"nextSteps":["Next step"]}'

# Get project summary
notes-agent summary

# Update documentation
notes-agent update
```

## 🔧 MCP Server Setup (For Cursor/AI Assistants)

### For Cursor IDE

1. **Install globally** (use install script above)

2. **Configure Cursor MCP settings:**

   Edit `~/Library/Application Support/Cursor/User/globalStorage/mcp.json` or create it:

   ```json
   {
     "mcpServers": {
       "notes-agent": {
         "command": "python3",
         "args": [
           "/Users/YOUR_USERNAME/.local/share/notes-agent/notes_agent_mcp.py",
           "mcp"
         ],
         "env": {
           "NOTES_AGENT_HOME": "/Users/YOUR_USERNAME/.local/share/notes-agent"
         }
       }
     }
   }
   ```

   Replace `YOUR_USERNAME` with your actual username.

3. **Restart Cursor** - The notes-agent will be available as an MCP tool

### For Other AI Assistants

The MCP server exposes these tools:
- `notes_agent_init` - Initialize notes-agent in a project
- `notes_agent_add_session` - Add a session entry
- `notes_agent_get_summary` - Get project summary
- `notes_agent_update` - Update documentation

## 🎯 How It Works

### Global Installation Structure

```
~/.local/share/notes-agent/     # Global installation
├── notes-agent.js              # Core script
├── notes_agent_mcp.py          # MCP server wrapper
├── generate_session.py         # Python helper
└── README.md                   # Documentation

~/.local/bin/notes-agent         # Global command (symlink)
```

### Project Structure (Auto-detected)

When you run `notes-agent` from a project directory:

1. **First time**: Run `notes-agent init` to create project-specific config
2. **Creates**: `notes-agent/` folder in project root with `config.json`
3. **Stores**: Project-specific sessions, notes, deployments

### Workflow

```bash
# In Project A
cd ~/projects/project-a
notes-agent init
notes-agent session --json '{"title":"..."}'

# In Project B  
cd ~/projects/project-b
notes-agent init
notes-agent session --json '{"title":"..."}'

# Each project has its own notes-agent/config.json
# But uses the same global command/tool
```

## 🔌 MCP Server Features

The MCP server allows AI assistants to:

1. **Auto-detect projects**: Finds project root automatically
2. **Initialize projects**: Sets up notes-agent in new projects
3. **Add sessions**: Programmatically add session summaries
4. **Get summaries**: Retrieve project documentation

### Example AI Assistant Usage

When working in a project, the AI can:

```python
# AI automatically detects project and adds session
notes_agent.add_session({
    "title": "Session Title",
    "summary": "What was accomplished",
    "decisions": ["Decision 1", "Decision 2"],
    "files": ["file1.py", "file2.js"],
    "blockers": ["Blocker 1"],
    "nextSteps": ["Next step 1"]
})
```

## 📝 Project Initialization

When you run `notes-agent init` in a project:

1. **Copies** notes-agent files to `project-root/notes-agent/`
2. **Creates** `notes-agent/config.json` with project info
3. **Generates** initial documentation files:
   - `PROJECT_NOTES.md`
   - `SESSION_LOG.md`
   - `DEPLOYMENT_LOG.md`

## ✅ Verification

After installation, verify it works:

```bash
# Check if command is available
which notes-agent
# Should output: /Users/YOUR_USERNAME/.local/bin/notes-agent

# Test in any project
cd /path/to/any/project
notes-agent summary
```

## 🆘 Troubleshooting

**Command not found:**
```bash
export PATH="$HOME/.local/bin:$PATH"
# Add to ~/.zshrc or ~/.bashrc
```

**Permission denied:**
```bash
chmod +x ~/.local/bin/notes-agent
```

**Node.js not found:**
- Install Node.js: `brew install node` (macOS)
- Or use Python version: `python3 ~/.local/share/notes-agent/notes_agent_mcp.py`

**Project not detected:**
- Make sure you're in a project directory
- Or specify project path: `notes-agent --project /path/to/project`

## 🌟 Benefits

✅ **One installation** - Works across all projects  
✅ **Auto-detection** - Finds project root automatically  
✅ **MCP integration** - Works with Cursor and other AI assistants  
✅ **No copying** - Global tool, project-specific configs  
✅ **Easy updates** - Update once, affects all projects  

---

**Install once, use everywhere!** 🚀


