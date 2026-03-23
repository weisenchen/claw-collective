# Step-by-Step Guide: Setting Up a 3-Agent Team

This guide demonstrates how to coordinate three agents (e.g., **Lead**, **Worker-1**, and **Worker-2**) to solve a problem using `claws`.

## Prerequisites
- **Git**: Installed on all 3 machines.
- **Python 3.10+**: Installed on all 3 machines.
- **`claws` CLI**: Installed on all 3 machines (`pip install -e .` in the `claws` directory).
- **Shared Repository**: A private GitHub/GitLab repository that all 3 machines can access.

---

## Step 1: Initialize the Lead Machine

On **Machine A** (The Team Lead):

1.  **Create the Workspace**:
    ```bash
    claws init project-alpha --remote git@github.com:your-org/project-alpha.git
    cd project-alpha
    ```

2.  **Register as Leader**:
    ```bash
    claws register --role Leader --name Lead-Agent
    ```

3.  **Create the Team**:
    ```bash
    claws team create alpha-team --description "Core Development Team" --leader Lead-Agent
    ```

4.  **Populate the Backlog**:
    ```bash
    claws task add alpha-team "Design API Schema" --owner Lead-Agent
    claws task add alpha-team "Implement Database Layer" # Unassigned
    claws task add alpha-team "Build Frontend UI" # Unassigned
    ```

---

## Step 2: Set Up Worker-1

On **Machine B** (Worker-1):

1.  **Clone and Enter Workspace**:
    ```bash
    git clone git@github.com:your-org/project-alpha.git
    cd project-alpha
    ```

2.  **Register the Machine**:
    ```bash
    claws register --role Worker --name Worker-1
    ```

3.  **Sync State**:
    ```bash
    claws sync pull
    ```

4.  **Claim a Task**:
    ```bash
    claws task start alpha-team <task-id-of-db-layer> --owner Worker-1
    ```

---

## Step 3: Set Up Worker-2

On **Machine C** (Worker-2):

1.  **Clone and Enter Workspace**:
    ```bash
    git clone git@github.com:your-org/project-alpha.git
    cd project-alpha
    ```

2.  **Register the Machine**:
    ```bash
    claws register --role Worker --name Worker-2
    ```

3.  **Sync State**:
    ```bash
    claws sync pull
    ```

4.  **Claim a Task**:
    ```bash
    claws task start alpha-team <task-id-of-frontend-ui> --owner Worker-2
    ```

---

## Step 4: Coordination in Action

### Monitoring Progress
The Lead can monitor everyone in real-time:
```bash
claws board live alpha-team
```

### Requesting Help
If **Worker-1** finishes early, they can message **Worker-2**:
```bash
claws inbox send alpha-team Worker-2 "Database is ready. You can now use the 'users' table." --from Worker-1
```

**Worker-2** reads the message:
```bash
claws inbox read alpha-team Worker-2
```

### Finalizing a Task
When **Worker-1** finishes the DB layer:
1.  **Scan and Push**: `claws sync push -m "Implemented database layer"`
2.  **Mark Done**: `claws task done alpha-team <task-id>`

---

## Step 5: Summary of Files
At the end of the day, your workspace will have:
- `STATUS.md`: Showing current activity for all 3 machines.
- `memory/global_context.md`: A log of completed work.
- `.openclaw/agent_directory.md`: A registry of the 3 machines.
- `roadmap/ACTIVE_SPRINT.md`: Up-to-date task statuses.
