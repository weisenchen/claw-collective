"""octeam lifecycle — agent state management.

Innovation: global state tracking via STATUS.md and ~/.octeam/ states.
"""

from __future__ import annotations

import os
from pathlib import Path

import click

from octeam.config import load_config
from octeam.locking import file_lock


def _update_status_md(workspace: Path, agent_id: str, new_status: str) -> None:
    status_path = workspace / "STATUS.md"
    if not status_path.exists():
        return

    with file_lock(status_path.with_suffix(".lock")):
        lines = status_path.read_text("utf-8").splitlines()
        updated = False
        new_lines = []
        for line in lines:
            if line.startswith(f"{agent_id}:"):
                new_lines.append(f"{agent_id}: {new_status}")
                updated = True
            else:
                new_lines.append(line)
        if not updated:
            new_lines.append(f"{agent_id}: {new_status}")
        status_path.write_text("\n".join(new_lines) + "\n", "utf-8")


@click.command("shutdown")
@click.option("--agent", "-a", help="Agent name")
@click.option("--team", "-t", help="Team name")
def cmd_shutdown(agent: str | None, team: str | None) -> None:
    """Shut down an agent and mark as OFFLINE."""
    config = load_config()
    workspace = Path(config.workspace_dir or os.getcwd())
    agent_id = agent or os.environ.get("OCTEAM_AGENT", "unknown")
    
    _update_status_md(workspace, agent_id, "OFFLINE")
    click.echo(f"⏹️  Agent '{agent_id}' marked as OFFLINE")


@click.command("idle")
@click.option("--agent", "-a", help="Agent name")
@click.option("--team", "-t", help="Team name")
def cmd_idle(agent: str | None, team: str | None) -> None:
    """Mark an agent as IDLE."""
    config = load_config()
    workspace = Path(config.workspace_dir or os.getcwd())
    agent_id = agent or os.environ.get("OCTEAM_AGENT", "unknown")

    _update_status_md(workspace, agent_id, "IDLE")
    click.echo(f"💤 Agent '{agent_id}' marked as IDLE")
