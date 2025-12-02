# 🚀 Quick Reference - Information Preservation System

## 📋 Daily Commands

### At Session Start (Automatic)
The AI will run this for you:
```bash
python3 scripts/check_backup_age.py
```

### Create Backup Manually
```bash
# Quick backup
python3 scripts/create_backup.py

# With description
python3 scripts/create_backup.py "BeforeAuthRefactor"
```

### Save Session Summary
Just tell the AI:
```
"Take a session summary"
"Save this session"
```

---

## 🎯 Just Tell the AI

These phrases trigger automatic actions:

| You Say | AI Does |
|---------|---------|
| "Check if backup is needed" | Runs check_backup_age.py |
| "Create a backup" | Runs create_backup.py |
| "Take a session summary" | Uses notes-agent command |
| "Check agent tasks" | Runs next_task.py |
| "Show recent backups" | Lists backups/ directory |

---

## 🛡️ The Three Rules

1. **Check backup age** at session start
2. **Save session summary** at session end  
3. **Create backup** before major changes

---

## 📂 File Locations

- **Backups**: `backups/V{X}.{Y}-Description-Timestamp/`
- **Scripts**: `scripts/create_backup.py`, `scripts/check_backup_age.py`
- **Session Log**: `SESSION_LOG.md`
- **Rules**: `.cursorrules`

---

## 🆘 Emergency Recovery

```bash
# List backups
ls -lt backups/ | head -5

# Restore a file
cp backups/V2.9-Name-Time/app.py .

# Restore everything
cp -r backups/V2.9-Name-Time/* .
```

---

## ✅ Current Status

```bash
# Latest backup
V2.9-InfoPreservationSystem-20251115_004740

# Size
13.2 MB

# Files backed up
14/14 (100%)

# Backup age
0.0 hours (just created!)
```

---

## 🎓 Next Steps

1. **Close this chat**
2. **Open NEW chat**
3. **Say**: "Check if backup is needed"
4. **Watch the magic!** ✨

---

*For full documentation, see: INFORMATION_PRESERVATION_SYSTEM.md*

