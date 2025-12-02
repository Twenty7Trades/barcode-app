# Notes Agent - Installation Guide for New Projects

This guide shows you how to copy the automated session documentation system to any new project.

## 📦 What to Copy

Copy the entire `notes-agent/` folder from this project to your new project root:

```
notes-agent/
├── notes-agent.js          # Main script with JSON input support
├── config.json             # Project configuration (will be updated)
├── generate_session.py      # Python helper script (optional)
└── README.md              # Documentation
```

**Also copy:**
- `package.json` (or merge the npm scripts into your existing package.json)

## 🚀 Quick Setup (3 Steps)

### Step 1: Copy Files

```bash
# From your current project (LLM-Generator1.0 2)
cd "/Applications/LLM-Generator1.0 2"

# Copy notes-agent folder to your new project
cp -r notes-agent /path/to/your/new/project/

# Copy package.json (or merge scripts manually)
# Option A: Copy entire package.json if project doesn't have one
cp package.json /path/to/your/new/project/

# Option B: Or merge scripts into existing package.json
# (See "Merging into Existing package.json" section below)
```

### Step 2: Initialize Configuration

```bash
cd /path/to/your/new/project

# Initialize the notes agent
npm run notes:init
# OR if no package.json yet:
node notes-agent/notes-agent.js init
```

This will prompt you for:
- Project Type (e.g., "Next.js", "React", "Python", "Flask", etc.)
- Production URL (optional)
- Staging URL (optional)

### Step 3: Update Config (Optional)

Edit `notes-agent/config.json` to customize:
- Project URLs
- Deployment platform info
- Common commands
- Related documentation links

```json
{
  "projectName": "your-project-name",
  "projectType": "Your Project Type",
  "urls": {
    "production": "https://your-app.com",
    "staging": "https://staging.your-app.com"
  },
  "commands": [
    "npm run dev",
    "npm run build"
  ],
  "documentation": [
    {
      "title": "Your Doc",
      "path": "docs/your-doc.md"
    }
  ]
}
```

## 📝 Merging into Existing package.json

If your project already has a `package.json`, add these scripts to the `"scripts"` section:

```json
{
  "scripts": {
    "notes:init": "node notes-agent/notes-agent.js init",
    "notes:update": "node notes-agent/notes-agent.js update",
    "notes:session": "node notes-agent/notes-agent.js session",
    "notes:note": "node notes-agent/notes-agent.js note",
    "notes:summary": "node notes-agent/notes-agent.js summary"
  }
}
```

## ✅ Verify Installation

```bash
# Check if it works
npm run notes:summary

# Should show:
# 📊 Project Summary
# ==================
# Project: your-project-name
# Type: Your Project Type
# Notes: 0
# Sessions: 0
# Deployments: 0
```

## 🎯 Usage

### Automated Session Summary (AI-Generated)

At the end of a work session, tell your AI assistant:
> "Generate session summary" or "Save today's session"

The AI will automatically create a session entry with:
- What was accomplished
- Key technical decisions
- Files changed
- Blockers encountered
- Next steps

### Manual Session Entry (Interactive)

```bash
npm run notes:session
```

Follow the prompts to manually enter session details.

### Programmatic Session Entry (JSON)

```bash
npm run notes:session '{"title":"Session Title","summary":"What was done","decisions":["Decision 1"],"files":["file1.py"],"blockers":[],"nextSteps":["Next step"]}'
```

### Update Documentation

```bash
npm run notes:update
```

Regenerates all documentation files from config.json.

## 📄 Generated Files

The system creates these files in your project root:
- `PROJECT_NOTES.md` - Main project notes, decisions, troubleshooting
- `SESSION_LOG.md` - Work session summaries
- `DEPLOYMENT_LOG.md` - Deployment history

**Note:** Add these to your `.gitignore` if you don't want them in version control, or commit them to preserve project knowledge.

## 🔧 Requirements

- **Node.js** installed (for running the notes-agent.js script)
- **npm** (for npm scripts - optional, can use node directly)

## 📋 Complete Copy Script

Here's a complete script to copy everything:

```bash
#!/bin/bash
# copy-notes-agent.sh

SOURCE_PROJECT="/Applications/LLM-Generator1.0 2"
TARGET_PROJECT="$1"

if [ -z "$TARGET_PROJECT" ]; then
    echo "Usage: ./copy-notes-agent.sh /path/to/new/project"
    exit 1
fi

echo "📦 Copying notes-agent to $TARGET_PROJECT..."

# Copy notes-agent folder
cp -r "$SOURCE_PROJECT/notes-agent" "$TARGET_PROJECT/"

# Check if package.json exists
if [ -f "$TARGET_PROJECT/package.json" ]; then
    echo "⚠️  package.json exists - you'll need to merge scripts manually"
    echo "Add these scripts to your package.json:"
    echo '  "notes:init": "node notes-agent/notes-agent.js init"'
    echo '  "notes:update": "node notes-agent/notes-agent.js update"'
    echo '  "notes:session": "node notes-agent/notes-agent.js session"'
    echo '  "notes:note": "node notes-agent/notes-agent.js note"'
    echo '  "notes:summary": "node notes-agent/notes-agent.js summary"'
else
    # Copy package.json
    cp "$SOURCE_PROJECT/package.json" "$TARGET_PROJECT/"
    echo "✅ Copied package.json"
fi

echo ""
echo "✅ Copy complete!"
echo ""
echo "Next steps:"
echo "1. cd $TARGET_PROJECT"
echo "2. npm run notes:init"
echo "3. Update notes-agent/config.json with your project info"
```

## 🎨 Customization Examples

### Python Project

```json
{
  "projectName": "my-python-app",
  "projectType": "Flask/Python",
  "commands": [
    "python3 app.py",
    "source venv/bin/activate && python3 app.py",
    "pytest"
  ]
}
```

### React/Next.js Project

```json
{
  "projectName": "my-react-app",
  "projectType": "Next.js",
  "commands": [
    "npm run dev",
    "npm run build",
    "npm run test"
  ],
  "urls": {
    "production": "https://myapp.com",
    "staging": "https://staging.myapp.com"
  }
}
```

### Node.js API Project

```json
{
  "projectName": "my-api",
  "projectType": "Node.js/Express",
  "commands": [
    "npm start",
    "npm run dev",
    "npm test"
  ],
  "deployment": {
    "platform": "AWS Lambda",
    "region": "us-east-1"
  }
}
```

## 💡 Tips

1. **Initialize early**: Set up notes-agent at the start of a project
2. **Update regularly**: Run `npm run notes:update` after making config changes
3. **Commit docs**: Consider committing `SESSION_LOG.md` and `PROJECT_NOTES.md` to preserve knowledge
4. **Use AI summaries**: Let your AI assistant generate session summaries automatically
5. **Track blockers**: Document blockers and solutions for future reference

## 🆘 Troubleshooting

**"npm: command not found"**
- Install Node.js from nodejs.org
- Or use `node notes-agent/notes-agent.js` directly

**"Cannot find module 'notes-agent/notes-agent.js'"**
- Make sure you're in the project root directory
- Verify `notes-agent/notes-agent.js` exists

**Config not updating**
- Run `npm run notes:update` after editing config.json
- Check that config.json is valid JSON

**Script not executable**
```bash
chmod +x notes-agent/notes-agent.js
chmod +x notes-agent/generate_session.py
```

---

**Ready to use!** Copy the `notes-agent/` folder to any project and start documenting your sessions automatically. 🚀


