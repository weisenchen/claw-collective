# `claws` Command Reference

## `init`
Scaffold a new OpenClaw team workspace.
- **Usage**: `claws init [PATH]`
- **Options**:
    - `--remote`, `-r`: GitHub remote URL to set as `origin`.
- **Created Files**: `STATUS.md`, `memory/`, `roadmap/`, `workspace/`, `.gitignore`, etc.

---

## `register` / `unregister`
Manage machine participation in a workspace.
- **`register`**:
    - **Options**:
        - `--name`, `-n`: Custom machine name (defaults to hostname).
        - `--role`, `-r`: `Leader`, `Worker`, `Tester`, `Researcher`.
        - `--ip`: Custom IP address (auto-detected).
        - `--workspace`, `-w`: Path to your workspace.
- **`unregister`**:
    - **Usage**: `claws unregister --name <NAME>`
    - Marks a machine as `OFFLINE` in `STATUS.md`.

---

## `sync`
Git-based synchronization with safety checks.
- **`sync push`**:
    - Scans for secrets via `secrets.py`.
    - commits all changes.
    - pushes to remote.
    - **Options**: `--message`, `-m`, `--auto` (no prompts).
- **`sync pull`**:
    - Fetches from remote and rebases.
    - **Options**: `--dry-run` to preview changes.
- **`sync status`**: Shows local changes and whether you are ahead/behind the remote.

---

## `team`
Manage team lifecycles.
- **`team create <NAME>`**:
    - **Options**: `--description`, `-d`, `--leader`, `-l`.
- **`team list`**: Shows all teams in a Rich table.
- **`team status <NAME>`**: Shows details for a specific team.
- **`team cleanup <NAME>`**: Deletes a team and all its data.

---

## `task`
Kanban-style task management with dependency tracking.
- **`task add <TEAM> <SUBJECT>`**:
    - **Options**: `--owner`, `-o`, `--blocked-by`, `-b` (comma-separated IDs).
- **`task start <TEAM> <TASK_ID>`**: Moves task to `in_progress`.
- **`task done <TEAM> <TASK_ID>`**: Marks task `completed` and **auto-unblocks** dependents.
- **`task list <TEAM>`**: Filterable list of tasks in a table.

---

## `inbox`
Inter-agent asynchronous messaging.
- **`inbox send <TEAM> <TO> <MESSAGE> --from <NAME>`**: Send a point-to-point message.
- **`inbox broadcast <TEAM> <MESSAGE> --from <NAME>`**: Message everyone except the sender.
- **`inbox read <TEAM> <AGENT>`**: Consume and display messages.
- **`inbox peek <TEAM> <AGENT>`**: View messages without removing them from the queue.

---

## `board`
Terminal-based Kanban dashboards.
- **`board show <TEAM>`**: Static view of the Kanban board with 4 columns: Pending, In Progress, Blocked, Completed.
- **`board live <TEAM>`**:
    - Auto-refreshing dashboard.
    - **Options**: `--interval`, `-i` (default: 3s).
