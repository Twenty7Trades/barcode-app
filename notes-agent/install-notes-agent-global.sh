#!/bin/bash
# install-notes-agent-global.sh
# Installs notes-agent as a global CLI tool accessible from anywhere

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_DIR="$HOME/.local/share/notes-agent"
BIN_DIR="$HOME/.local/bin"

echo "📦 Installing Notes Agent globally..."

# Create installation directory
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Copy notes-agent files
echo "Copying files..."
cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/" 2>/dev/null || true

# Ensure notes-agent.js is executable
chmod +x "$INSTALL_DIR/notes-agent.js" 2>/dev/null || true
chmod +x "$INSTALL_DIR/notes_agent_mcp.py" 2>/dev/null || true
chmod +x "$INSTALL_DIR/generate_session.py" 2>/dev/null || true

# Create global wrapper script
cat > "$BIN_DIR/notes-agent" << 'EOFW'
#!/bin/bash
# Global notes-agent wrapper

NOTES_AGENT_HOME="$HOME/.local/share/notes-agent"
NOTES_AGENT_PY="$NOTES_AGENT_HOME/notes_agent_mcp.py"

# If Python script exists, use it (preferred)
if [ -f "$NOTES_AGENT_PY" ]; then
    python3 "$NOTES_AGENT_PY" "$@"
    exit $?
fi

# Fallback to Node.js
NOTES_AGENT_JS="$NOTES_AGENT_HOME/notes-agent.js"
if [ -f "$NOTES_AGENT_JS" ]; then
    # Detect project root with notes-agent folder
    PROJECT_ROOT=$(pwd)
    while [ "$PROJECT_ROOT" != "/" ]; do
        if [ -d "$PROJECT_ROOT/notes-agent" ] && [ -f "$PROJECT_ROOT/notes-agent/notes-agent.js" ]; then
            node "$PROJECT_ROOT/notes-agent/notes-agent.js" "$@"
            exit $?
        fi
        PROJECT_ROOT=$(dirname "$PROJECT_ROOT")
    done
    
    # If no project found, use global
    node "$NOTES_AGENT_JS" "$@"
else
    echo "❌ notes-agent not found. Please run install-notes-agent-global.sh"
    exit 1
fi
EOFW

chmod +x "$BIN_DIR/notes-agent"

# Ensure ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo "⚠️  Add this to your ~/.zshrc or ~/.bashrc:"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Then run: source ~/.zshrc"
    echo ""
fi

echo ""
echo "✅ Notes Agent installed globally!"
echo ""
echo "Usage:"
echo "  notes-agent init              # Initialize in current project"
echo "  notes-agent session --json '{\"title\":\"...\"}'  # Add session"
echo "  notes-agent summary           # Show project summary"
echo ""
echo "From any project directory, run:"
echo "  notes-agent init"
echo "  notes-agent session --json '{\"title\":\"Session Title\",\"summary\":\"What was done\"}'"
echo ""

