"""Claw Collective template — TOML-based team templates.

Innovation: flat, readable TOML format for defining team structure.
"""

from __future__ import annotations

import os
from pathlib import Path

import click
try:
    import tomllib
except ImportError:
    import tomli as tomllib


@click.command("launch")
@click.argument("template")
@click.option("--team", "-t", help="Team name (overrides template name)")
def cmd_launch(template: str, team: str | None) -> None:
    """Launch a team defined in a TOML template file."""
    p = Path(template)
    if not p.exists():
        click.echo(f"❌ Template '{template}' not found")
        return

    try:
        content = p.read_text("utf-8")
        data = tomllib.loads(content)
    except Exception as e:
        click.echo(f"❌ Error parsing TOML: {e}")
        return

    team_name = team or data.get("team", {}).get("name")
    if not team_name:
        click.echo("❌ No team name specified in template or CLI")
        return

    click.echo(f"🚀 Launching team '{team_name}' from template...")

    # Create team
    from claws.team import team_create
    team_create.callback(team_name, data.get("team", {}).get("description", ""), data.get("team", {}).get("leader", ""))

    # Spawn agents
    from claws.spawn import cmd_spawn
    agents = data.get("agents", [])
    for agent in agents:
        agent_name = agent.get("name")
        task = agent.get("task", "Initial task")
        command = agent.get("command", "")
        cmd_args = tuple(command.split()) if command else ()
        
        click.echo(f"  - Spawning agent '{agent_name}'...")
        cmd_spawn.callback(team_name, agent_name, task, False, False, cmd_args)

    click.echo(f"✅ Team '{team_name}' launched successfully!")
