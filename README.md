# user-manual

Persistent profile management for OpenClaw using Novyx memory.

## Features

- Persistent USER.md profile
- Auto-injection on startup
- Natural language updates
- Cloud backup via Novyx

## How It Works

The user-manual skill maintains a `USER.md` file that stores user preferences, project context, and working style. It automatically injects this context at the start of every conversation so your AI agent already knows who you are.

When you tell the agent something about yourself — your preferred language, your tech stack, how you like responses formatted — it updates the profile automatically using natural language.

All changes are backed up to Novyx, so your profile persists across sessions and devices.

## Install

```bash
clawhub install user-manual
```

Or manually:

```bash
git clone https://github.com/novyxlabs/user-manual.git skills/user-manual
cd skills/user-manual && pip install -r requirements.txt
```

## Configuration

Set your Novyx API key:

```bash
echo "NOVYX_API_KEY=nram_your_key_here" >> .env
```

Get a free API key at [novyxlabs.com](https://novyxlabs.com).

## License

MIT
