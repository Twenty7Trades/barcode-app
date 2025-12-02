# Notes Agent

A reusable documentation generator for preserving project knowledge and context across work sessions.

## Quick Start

1. **Copy the `notes-agent/` folder to your project root**
2. **Run initialization:**
   ```bash
   node notes-agent/notes-agent.js init
   ```
3. **After each work session, add a summary:**
   ```bash
   node notes-agent/notes-agent.js session
   ```

## Usage

### Initialize Documentation
```bash
node notes-agent/notes-agent.js init
```
Creates initial documentation files and config. Prompts for basic project information.

### Update Documentation
```bash
node notes-agent/notes-agent.js update
```
Refreshes all documentation files from the current config.json.

### Add Session Summary
```bash
node notes-agent/notes-agent.js session
```
Interactive prompt to add a work session summary. Captures:
- What was done
- Key decisions made
- Files changed
- Blockers encountered
- Next steps

### Add Important Note
```bash
node notes-agent/notes-agent.js note
```
Add an important decision, fix, or gotcha. Useful for:
- Important architectural decisions
- Bug fixes that took time to solve
- Configuration changes
- Workarounds

### Show Summary
```bash
node notes-agent/notes-agent.js summary
```
Quick overview of project documentation status.

## Generated Files

- `PROJECT_NOTES.md` - Main project notes, decisions, and troubleshooting
- `DEPLOYMENT_LOG.md` - Deployment history and changes
- `SESSION_LOG.md` - Work session summaries

## Configuration

Edit `notes-agent/config.json` to customize:
- Project URLs (production, staging, etc.)
- Deployment info (platform, app ID, region)
- Credential locations (where secrets are stored)
- Common commands
- Related documentation links

## Best Practices

1. **Run after each session**: `node notes-agent/notes-agent.js session`
   - Captures context before switching projects
   - Helps remember what was done

2. **Add important decisions**: `node notes-agent/notes-agent.js note`
   - Documents why things were done a certain way
   - Helps future you (or others) understand decisions

3. **Update before switching projects**: `node notes-agent/notes-agent.js update`
   - Ensures all docs are current
   - Good checkpoint before context switching

4. **Commit documentation**: Keep docs in version control
   - `PROJECT_NOTES.md`, `DEPLOYMENT_LOG.md`, `SESSION_LOG.md`
   - Consider excluding `notes-agent/config.json` if it contains sensitive info

5. **Review before starting work**: Check `SESSION_LOG.md` for recent context

## Porting to New Project

1. **Copy entire `notes-agent/` folder** to new project root
2. **Run initialization:**
   ```bash
   node notes-agent/notes-agent.js init
   ```
3. **Update `config.json`** with project-specific info:
   - URLs
   - Deployment platform details
   - Common commands
   - Related documentation
4. **Start documenting!**

## Example Workflow

```bash
# Morning: Start new session
git pull
node notes-agent/notes-agent.js session
# ... do work ...

# Afternoon: Before switching projects
node notes-agent/notes-agent.js session
node notes-agent/notes-agent.js update
git add PROJECT_NOTES.md SESSION_LOG.md DEPLOYMENT_LOG.md
git commit -m "Update project documentation"
```

## Tips

- **Be specific**: Include file paths, error messages, solutions
- **Reference related docs**: Link to other markdown files when relevant
- **Track blockers**: Document what blocked you and how you solved it
- **Note next steps**: Helps pick up where you left off

## Troubleshooting

**Script not executable?**
```bash
chmod +x notes-agent/notes-agent.js
```

**Config file not found?**
Run `node notes-agent/notes-agent.js init` first.

**Want to edit manually?**
Edit `notes-agent/config.json` directly, then run `update` to regenerate docs.

---

*Keep your project knowledge safe! 📝*

