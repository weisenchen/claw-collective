"""Claw Collective register / unregister — machine registration.

Innovation: vendor requires manual file editing. We auto-detect hostname/IP.
"""

from __future__ import annotations

import socket
from pathlib import Path

import click


def _detect_hostname() -> str:
    return socket.gethostname()


def _detect_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def _find_workspace() -> Path:
    """Walk up from cwd to find a workspace with STATUS.md."""
    p = Path.cwd()
    for _ in range(10):
        if (p / "STATUS.md").exists():
            return p
        if p.parent == p:
            break
        p = p.parent
    return Path.cwd()


@click.command("register")
@click.option("--name", "-n", default="", help="Machine name (auto-detected if empty)")
@click.option("--role", "-r", default="Worker", type=click.Choice(["Leader", "Worker", "Tester", "Researcher"]))
@click.option("--ip", default="", help="IP address (auto-detected if empty)")
@click.option("--workspace", "-w", default="", help="Workspace path (auto-detected if empty)")
def cmd_register(name: str, role: str, ip: str, workspace: str) -> None:
    """Register this machine with the team workspace."""
    ws = Path(workspace) if workspace else _find_workspace()
    machine_name = name or _detect_hostname()
    machine_ip = ip or _detect_ip()

    # Update agent_directory.md
    agent_dir = ws / ".openclaw" / "agent_directory.md"
    if agent_dir.exists():
        content = agent_dir.read_text("utf-8")
        if machine_name not in content:
            with open(agent_dir, "a", encoding="utf-8") as f:
                f.write(f"| {machine_name} | {machine_ip} | {role} | Idle |\n")
            click.echo(f"📋 Added {machine_name} to agent directory")
        else:
            click.echo(f"⚠️  {machine_name} already registered")
            return

    # Update STATUS.md
    status_file = ws / "STATUS.md"
    if status_file.exists():
        with open(status_file, "a", encoding="utf-8") as f:
            f.write(f"\n{machine_name} ({role}): IDLE - Available for tasks.\n")
        click.echo(f"💓 Added {machine_name} to STATUS.md")

    click.echo(f"✅ Registered: {machine_name} ({role}) @ {machine_ip}")


@click.command("unregister")
@click.option("--name", "-n", required=True, help="Machine name to remove")
@click.option("--workspace", "-w", default="", help="Workspace path")
def cmd_unregister(name: str, workspace: str) -> None:
    """Remove a machine from the team workspace."""
    ws = Path(workspace) if workspace else _find_workspace()

    # Update STATUS.md — mark as OFFLINE
    status_file = ws / "STATUS.md"
    if status_file.exists():
        lines = status_file.read_text("utf-8").splitlines()
        new_lines = []
        for line in lines:
            if line.startswith(name):
                new_lines.append(f"{name}: OFFLINE")
            else:
                new_lines.append(line)
        status_file.write_text("\n".join(new_lines) + "\n", "utf-8")

    click.echo(f"✅ {name} set to OFFLINE")
