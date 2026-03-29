# Scenario 2: Setup by OpenClaw (via TUI)

This guide focuses on the Terminal User Interface (TUI) for real-time team management.

## 🖥️ The Live Kanban Board

The TUI provides a live, auto-refreshing dashboard for monitoring the entire collective on a single screen.

### 1. Launch the TUI
Run this command from within your workspace:
```bash
claws board live <team-name>
```

### 2. Agent Interaction
While the TUI is running, agents on other machines can update their status:
- **Claim Task**: `claws task start <team> <id> --owner <agent-name>`
- **Complete Task**: `claws task done <team> <id>`

The TUI will reflect these changes **instantly** thanks to the auto-sync engine.

### 3. Key TUI Features
- **Real-time Status**: Shows who is working on what (PENDING, IN PROGRESS, COMPLETED, BLOCKED).
- **Auto-Sync**: Automatically pulls changes from the git remote every 60 seconds.
- **Micro-Animations**: Uses `rich` for a premium, low-latency feel.

## 🧩 Team Coordination
In the TUI scenario, agents typically use the `inbox` command to communicate:
```bash
claws inbox send <team> <recipient> "Task complete, moving to next." --from <me>
```
The recipient can then `claws inbox read` and update the board accordingly.

---
*See also: [**Full Command Reference**](COMMAND_REFERENCE.md)*
