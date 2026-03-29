# Scenario 1: Setup by OpenClaw Agent (via Telegram)

This guide explains how to use the Telegram Orchestration layer to spawn and command agents.

## 🚀 Overview

The Telegram bridge allows a human or a leader agent to manage the collective using natural language commands. 

### 1. Configure the Telegram Bridge
Ensure your bot token is set in your environment:
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
```

### 2. Launch the Bridge
Run the orchestration service in your workspace:
```bash
claws orchestration start
```

### 3. Command via Telegram
Send instructions to your bot:
> "Create a new research team for the AI Ethics project. Spawn a Lead Agent and three Security Reviewers."

### 4. Agent Autonomous Setup
Agents will follow the [AGENT_SELF_SETUP](AGENT_SELF_SETUP.md) protocol:
- Clone repo
- Run `./scripts/bootstrap.sh`
- `source .venv/bin/activate`
- `claws register`
- Start working on assigned tasks.

## 🔄 The Golden Loop (Auto-Sync)
Every command sent via Telegram triggers the **Golden Loop** (PULL → LOCK → WORK → LOG → PUSH), ensuring that the shared State in `.openclaw/` is always up to date across all machines.

---
*See also: [**Full Command Reference**](COMMAND_REFERENCE.md)*
