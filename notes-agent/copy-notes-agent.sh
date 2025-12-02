#!/bin/bash
# copy-notes-agent.sh
# Copies the notes-agent system to a new project

SOURCE_PROJECT="/Applications/LLM-Generator1.0 2"
TARGET_PROJECT="$1"

if [ -z "$TARGET_PROJECT" ]; then
    echo "❌ Usage: ./copy-notes-agent.sh /path/to/new/project"
    exit 1
fi

if [ ! -d "$SOURCE_PROJECT/notes-agent" ]; then
    echo "❌ Error: notes-agent not found in $SOURCE_PROJECT"
    exit 1
fi

echo "📦 Copying notes-agent to $TARGET_PROJECT..."

# Create target directory if it doesn't exist
mkdir -p "$TARGET_PROJECT"

# Copy notes-agent folder
cp -r "$SOURCE_PROJECT/notes-agent" "$TARGET_PROJECT/"
echo "✅ Copied notes-agent folder"

# Check if package.json exists
if [ -f "$TARGET_PROJECT/package.json" ]; then
    echo ""
    echo "⚠️  package.json already exists in target project"
    echo ""
    echo "Please add these scripts to your package.json 'scripts' section:"
    echo ""
    echo '  "notes:init": "node notes-agent/notes-agent.js init",'
    echo '  "notes:update": "node notes-agent/notes-agent.js update",'
    echo '  "notes:session": "node notes-agent/notes-agent.js session",'
    echo '  "notes:note": "node notes-agent/notes-agent.js note",'
    echo '  "notes:summary": "node notes-agent/notes-agent.js summary"'
    echo ""
else
    # Copy package.json if it doesn't exist
    cp "$SOURCE_PROJECT/package.json" "$TARGET_PROJECT/"
    echo "✅ Copied package.json"
fi

# Make scripts executable
chmod +x "$TARGET_PROJECT/notes-agent/notes-agent.js" 2>/dev/null
chmod +x "$TARGET_PROJECT/notes-agent/generate_session.py" 2>/dev/null

echo ""
echo "✅ Copy complete!"
echo ""
echo "📋 Next steps:"
echo "1. cd $TARGET_PROJECT"
echo "2. npm run notes:init"
echo "3. Update notes-agent/config.json with your project-specific information"
echo ""
echo "💡 See notes-agent/INSTALLATION_GUIDE.md for detailed instructions"


