# `octeam` Workflow Examples

Practical coordination patterns for agents using the `octeam` CLI.

## 📝 1. Submitting a Plan for Approval

When proposing significant changes, use the `plan` workflow:

```bash
# Submit a plan
octeam plan submit my-team "Migrate the database to PostgreSQL" --author "ArchitectAgent"

# List plans to see the ID
octeam plan list my-team

# (A human or lead agent approves)
octeam plan approve my-team <plan-id>
```

## 🚀 2. Spawning a Sub-Agent

Delegate tasks to a sub-agent with isolated environment:

```bash
octeam spawn --team my-team --name "Worker-1" --task "Run tests and report results" "pytest"
```

This creates a dedicated `tmux` window and a `git worktree` for the task.

## 📢 3. Team-wide Broadcasts

Notify everyone on the team about an event:

```bash
octeam inbox broadcast my-team "Deployment started on production" --from "DeployAgent"
```

## 🗾 4. Using Team Templates

Launch multiple agents at once using a TOML template:

`my-team.toml`:
```toml
[team]
name = "my-team"
description = "Web app development"
leader = "LeadAgent"

[[agents]]
name = "FrontendAgent"
task = "Implement login page"
command = "npm run dev"

[[agents]]
name = "BackendAgent"
task = "API endpoints for auth"
command = "python app.py"
```

Launch:
```bash
octeam launch my-team.toml
```

## 🔄 5. Merging Collective Work

When a worker finishes their worktree-isolated task:

```bash
# In the worker's worktree:
octeam ws save -m "Finished implementation of X"
octeam ws merge main
```

---

> [!NOTE]
> All changes are automatically recorded in the `global_context.md` when using the `sync` commands or when `octeam` components interact with the workspace.
