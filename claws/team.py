"""Claw Collective team — team lifecycle management.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from claws.config import data_dir
from claws.locking import atomic_write_json, file_lock, read_json


def _team_dir(team: str) -> Path:
    d = data_dir() / "teams" / team
    d.mkdir(parents=True, exist_ok=True)
    return d


def _team_config_path(team: str) -> Path:
    return _team_dir(team) / "config.json"


def _lock_path(team: str) -> Path:
    return _team_dir(team) / "team.lock"


@click.group("team")
def cmd_team() -> None:
    """Team lifecycle management."""
    pass


@cmd_team.command("create")
@click.argument("name")
@click.option("--description", "-d", default="", help="Team description")
@click.option("--leader", "-l", default="", help="Leader agent name")
def team_create(name: str, description: str, leader: str) -> None:
    """Create a new team."""
    config_path = _team_config_path(name)
    if config_path.exists():
        click.echo(f"⚠️  Team '{name}' already exists")
        return

    config = {
        "name": name,
        "description": description,
        "leader": leader,
        "members": [leader] if leader else [],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    with file_lock(_lock_path(name)):
        atomic_write_json(config_path, config)

    # Create subdirectories
    (_team_dir(name) / "tasks").mkdir(exist_ok=True)
    (_team_dir(name) / "inboxes").mkdir(exist_ok=True)
    (_team_dir(name) / "events").mkdir(exist_ok=True)

    click.echo(f"✅ Team '{name}' created" + (f" (leader: {leader})" if leader else ""))


@cmd_team.command("list")
def team_list() -> None:
    """List all teams."""
    teams_root = data_dir() / "teams"
    if not teams_root.exists():
        click.echo("No teams found")
        return

    console = Console()
    table = Table(title="Teams")
    table.add_column("Name", style="cyan")
    table.add_column("Leader")
    table.add_column("Members")
    table.add_column("Created")

    for d in sorted(teams_root.iterdir()):
        if not d.is_dir():
            continue
        config_path = d / "config.json"
        if not config_path.exists():
            continue
        try:
            cfg = json.loads(config_path.read_text("utf-8"))
            table.add_row(
                cfg.get("name", d.name),
                cfg.get("leader", ""),
                str(len(cfg.get("members", []))),
                cfg.get("created_at", "")[:10],
            )
        except Exception:
            table.add_row(d.name, "?", "?", "?")

    console.print(table)


@cmd_team.command("status")
@click.argument("name")
def team_status(name: str) -> None:
    """Show team status and members."""
    config_path = _team_config_path(name)
    if not config_path.exists():
        click.echo(f"❌ Team '{name}' not found")
        return

    cfg = json.loads(config_path.read_text("utf-8"))
    console = Console()
    console.print(f"[bold]Team:[/bold] {cfg.get('name')}")
    console.print(f"[bold]Leader:[/bold] {cfg.get('leader', 'none')}")
    console.print(f"[bold]Description:[/bold] {cfg.get('description', '')}")
    console.print(f"[bold]Members:[/bold] {', '.join(cfg.get('members', []))}")
    console.print(f"[bold]Created:[/bold] {cfg.get('created_at', '')}")

    # Count tasks
    from claws.task import _list_all_tasks
    tasks = _list_all_tasks(name)
    console.print(f"[bold]Tasks:[/bold] {len(tasks)}")


@cmd_team.command("cleanup")
@click.argument("name")
@click.option("--force", is_flag=True, help="Skip confirmation")
def team_cleanup(name: str, force: bool) -> None:
    """Delete a team and all its data."""
    team_path = _team_dir(name)
    if not team_path.exists():
        click.echo(f"❌ Team '{name}' not found")
        return

    if not force and not click.confirm(f"Delete team '{name}' and all data?"):
        return

    import shutil
    shutil.rmtree(team_path)
    click.echo(f"🗑️  Team '{name}' deleted")
