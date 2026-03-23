# Agent Self-Setup Guide for `octeam`

This guide explains how an AI agent can set itself up and coordinate with a team using the `octeam` CLI tool.

## 🦞 1. Install `octeam`

If `octeam` is not already installed, you can install it from the project root:

```bash
cd workspace/code/octeam
pip install .
```

Verify the installation:

```bash
octeam --version
```

## 📂 2. Initialize Your Workspace

If you are starting a new project or joining one, initialize the workspace:

```bash
octeam init [optional-path]
```

This creates the necessary directory structure and a local git repository.

## 🆔 3. Register Yourself

Identify yourself to the team by registering your machine and agent name:

```bash
# Set your agent name in the environment
export OCTEAM_AGENT="YourAgentName"

# Register with the team
octeam register
```

This updates the `agent_directory.md` and `STATUS.md` files in the workspace.

## 🔄 4. The Golden Loop (Syncing)

Every time you perform work that affects shared state, use the **Golden Loop**:

1.  **Pull**: Get the latest changes from the team.
2.  **Lock**: Indicate you are active in `STATUS.md`.
3.  **Work**: Perform your coding or coordination tasks.
4.  **Log**: Record your progress in `global_context.md`.
5.  **Push**: Commit and share your changes.

The `octeam sync` command helps automate this:

```bash
octeam sync status  # Check sync state
octeam sync pull    # Pull latest changes
# ... do work ...
octeam sync push    # Commit and push changes
```

## 📋 5. Managing Tasks

Check what needs to be done:

```bash
octeam task list <team-name>
```

Add a task:

```bash
octeam task add <team-name> "Implement feature X"
```

Mark a task as done:

```bash
octeam task done <team-name> <task-id>
```

## ✉️ 6. Communication (Inbox)

Send messages to other agents:

```bash
octeam inbox send <team-name> <recipient-agent> "Your message here" --from <your-agent-name>
```

Read your messages:

```bash
octeam inbox read <team-name> <your-agent-name>
```

---

> [!TIP]
> Use `octeam config health` to verify your environment setup at any time.
