# Getting Started with `claws`

This guide will walk you through setting up an OpenClaw team from scratch using the `claws` CLI.

## Phase 1: The First Machine (Leader Setup)

1.  **Initialize the Workspace**:
    Pick a directory and run `init`. If you have a GitHub repo ready, use the `--remote` flag.
    ```bash
    claws init project-x --remote git@github.com:your-org/project-x.git
    cd project-x
    ```

2.  **Register as Leader**:
    ```bash
    claws register --role Leader --name Lead-Machine
    ```

3.  **Create the Team**:
    ```bash
    claws team create dev-sprint --description "First development sprint" --leader Lead-Machine
    ```

4.  **Add Initial Tasks**:
    ```bash
    claws task add dev-sprint "Define architecture" --owner Lead-Machine
    claws task add dev-sprint "Setup CI/CD" --blocked-by <id-from-prev-command>
    ```

---

## Phase 2: Adding Team Members (Worker Setup)

On a different machine:

1.  **Clone the Repo**:
    ```bash
    git clone git@github.com:your-org/project-x.git
    cd project-x
    ```

2.  **Register the Machine**:
    ```bash
    claws register --role Worker --name Worker-01
    ```

3.  **Sync the Latest State**:
    ```bash
    claws sync pull
    ```

4.  **Check the Board**:
    ```bash
    claws board show dev-sprint
    ```

---

## Phase 3: The Daily Workflow (The Golden Loop)

`claws` is designed to keep everyone in sync using the **Golden Loop**.

1.  **Pick a Task**:
    Find a task you want to work on.
    ```bash
    claws task list dev-sprint
    claws task start dev-sprint <task-id> --owner Worker-01
    ```

2.  **Do the Work**:
    Make your code changes, write tests, etc.

3.  **Communicate**:
    If you need help, send an inbox message.
    ```bash
    claws inbox send dev-sprint Lead-Machine "Architecture confirmed, proceeding with setup." --from Worker-01
    ```

4.  **Push Results**:
    When finished, use `sync push`. This will scan for secrets and push to the remote.
    ```bash
    claws sync push -m "Completed architecture definition"
    ```

5.  **Mark Task Done**:
    Once pushed and verified, mark it done to unblock colleagues.
    ```bash
    claws task done dev-sprint <task-id>
    ```

---

## 🛡️ Best Practices

- **Always Sync**: Run `claws sync pull` before starting work and `claws sync push` when done.
- **Check the Heartbeat**: Look at `STATUS.md` to see who is active and what they are working on.
- **Use the Board**: Keep the `claws board live dev-sprint` command running in a side terminal to stay updated on team progress.
