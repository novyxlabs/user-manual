---
name: user-manual
description: Manage the user's persistent profile (USER.md) and recall preferences using Novyx memory. Automatically injects context and syncs updates.
metadata: { "openclaw": { "emoji": "📖", "requires": { "bins": ["python3"] } } }
---

# User Manual 📖

The **User Manual** skill manages your persistent profile (`USER.md`). It ensures the AI always knows who you are, your preferences, and your rules—even in new sessions.

## 🚀 Key Features

*   **Auto-Injection:** Reads `USER.md` at startup so the AI knows you instantly.
*   **Natural Updates:** Just say "I prefer Python" or "My AWS region is us-east-1".
*   **Cloud Backup:** Syncs every update to Novyx for version history and cross-device recall.
*   **Stats:** Shows your memory usage and profile health.

## 🛠️ Usage

### 1. View Profile & Stats

```bash
# Show current profile stats (Memory usage, last update)
user-manual stats

# Read the full profile
user-manual read
```

### 2. Update Profile

```bash
# Append a new preference or fact
user-manual update "I prefer TypeScript over JavaScript"

# Set a specific section
user-manual set "Preferences" "Always use async/await, no callbacks."
```

### 3. Recall Specifics

```bash
# Find a specific preference
user-manual find "database"
```

## ⚙️ Configuration

The skill relies on `USER.md` in your workspace root. If it doesn't exist, it will be created.

## 📦 Novyx Integration

This skill uses the `novyx` python library to:
1.  **Store** every profile update as a durable memory.
2.  **Recall** relevant context when you ask questions.
3.  **Track** usage against your Free/Pro tier limits.
