"""octeam init — scaffold a new OpenClaw team workspace.

Creates the full directory structure, config files, and git repo in one command.
Innovation: vendor repos require 4 separate installs + manual file creation.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import click


GITIGNORE_CONTENT = """\
# OpenClaw System Files
.openclaw/
*.log
*.db
sessions/
_reference/

# Credentials
.env
credentials/
tokens.json

# OS
.DS_Store
Thumbs.db
"""

TEAM_RULES_CONTENT = """\
# THE OPENCLAW LAW (v1.0)

1. Set `STATUS.md` to ACTIVE before starting work.
2. Summarize results in `memory/global_context.md` when finished.
3. Document all design decisions in `workspace/docs`.
4. Ensure all code in `workspace/code` passes tests.
"""

STATUS_CONTENT = """\
# STATUS (The Heartbeat)

Update this before starting work.

"""

CONTEXT_CONTENT = """\
# Global Context (Long-Term Memory)

Append a 2-sentence summary after every completed task.

---

"""

AGENT_DIR_CONTENT = """\
# Agent Directory

| Machine | IP | Role | Status |
|---|---|---|---|
"""

BACKLOG_CONTENT = """\
# Task Backlog

- [ ] Define project goals
"""

SPRINT_CONTENT = """\
# Active Sprint

No active tasks yet.
"""


DIRS = [
    ".openclaw",
    "memory",
    "memory/archive",
    "roadmap",
    "workspace/code",
    "workspace/docs",
]

FILES = {
    ".gitignore": GITIGNORE_CONTENT,
    ".openclaw/team_rules.md": TEAM_RULES_CONTENT,
    ".openclaw/agent_directory.md": AGENT_DIR_CONTENT,
    "STATUS.md": STATUS_CONTENT,
    "memory/global_context.md": CONTEXT_CONTENT,
    "roadmap/BACKLOG.md": BACKLOG_CONTENT,
    "roadmap/ACTIVE_SPRINT.md": SPRINT_CONTENT,
}


@click.command("init")
@click.argument("path", default=".", type=click.Path())
@click.option("--remote", "-r", default="", help="GitHub remote URL to set as origin")
def cmd_init(path: str, remote: str) -> None:
    """Scaffold a new OpenClaw team workspace."""
    root = Path(path).resolve()
    root.mkdir(parents=True, exist_ok=True)

    # Create directories
    for d in DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)
    click.echo(f"📂 Created directory structure at {root}")

    # Create files (only if they don't exist)
    created = 0
    for rel_path, content in FILES.items():
        fp = root / rel_path
        if not fp.exists():
            fp.write_text(content, "utf-8")
            created += 1
    click.echo(f"📝 Created {created} files")

    # Init git
    git_dir = root / ".git"
    if not git_dir.exists():
        subprocess.run(["git", "init"], cwd=root, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=root, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "octeam init: scaffold workspace"],
            cwd=root, capture_output=True,
        )
        click.echo("🔧 Initialized git repository")

    # Set remote
    if remote:
        subprocess.run(
            ["git", "remote", "add", "origin", remote],
            cwd=root, capture_output=True,
        )
        click.echo(f"🔗 Set remote: {remote}")

    click.echo("✅ Workspace ready!")
