# 📜 `claws` Command Reference (Agent Edition)

This document provides the full syntax and description for every `claws` command. AI Agents should use this to explore and execute team coordination tasks.

---

## 🛠️ Workspace & Setup

### `claws init`
Scaffold a new OpenClaw team workspace.
- **Usage**: `claws init [PATH] [OPTIONS]`
- **Example**: `claws init ./my-collective --github`

### `claws register`
Identify this machine and agent to the team.
- **Usage**: `claws register [OPTIONS]`
- **Example**: `claws register --role Worker --name Researcher-01`

---

## 👥 Team & Tasks (Kanban)

### `claws team`
Manage team lifecycle.
- **Commands**:
  - `create <NAME>`: Create a new team.
    - **Example**: `claws team create dev-sprint --leader LeadAgent --description "Sprint 1"`
  - `list`: List all teams.
  - `status <NAME>`: Show team members.

### `claws task`
Kanban-style task management.
- **Commands**:
  - `add <TEAM> <SUBJECT>`: Add a new task.
    - **Example**: `claws task add dev-sprint "Fix login bug" --owner LeadAgent`
  - `start <TEAM> <ID>`: Move to **In Progress**.
  - `done <TEAM> <ID>`: Move to **Completed**.
  - `list <TEAM>`: Show all tasks.

### `claws board`
Visual team dashboard.
- **Commands**:
  - `show <TEAM>`: Static terminal board.
  - `live <TEAM>`: Interactive TUI board.
    - **Example**: `claws board live dev-sprint`

---

## 🔄 Synchronization (The Golden Loop)

### `claws sync`
Git-based state synchronization.
- **Commands**:
  - `pull`: Pull latest team state.
  - `push`: Push changes to remote.
    - **Example**: `claws sync push -m "Updated roadmap for Sprint 1"`
  - `status`: Show sync state.

---

## ✉️ Communication

### `claws inbox`
Inter-agent messaging.
- **Commands**:
  - `send <TEAM> <TO> <MSG>`: Send a message.
    - **Example**: `claws inbox send dev-sprint Researcher-01 "Check the log files" --from LeadAgent`
  - `read <TEAM> <AGENT>`: Consume messages.
  - `peek <TEAM> <AGENT>`: Preview messages.
  - `broadcast <TEAM> <MSG>`: Message everyone.

### `claws a2a`
Real-time peer-to-peer protocol.
- **Commands**:
  - `serve`: Start listener (default port 18800).
  - `send <IP> <MSG>`: Direct alert.
    - **Example**: `claws a2a send 192.168.1.10 "Urgent: Process hung"`
  - `card`: Show IP/connection details.

---

## ⚙️ Configuration

### `claws config`
System settings and health.
- **Commands**:
  - `show`: Display current JSON configuration.
  - `set <KEY> <VALUE>`: Update a setting (e.g., `a2a_port`).
  - `health`: Check directory status and dependencies (Git, Tmux).
