"""Claw Collective inbox — inter-agent messaging.

Innovation: simpler API (send/read/broadcast/peek), atomic file ops.
"""

from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

from claws.config import data_dir


def _inbox_dir(team: str, agent: str) -> Path:
    d = data_dir() / "teams" / team / "inboxes" / agent
    d.mkdir(parents=True, exist_ok=True)
    return d


def _deliver(team: str, to: str, from_agent: str, content: str, msg_type: str = "message") -> None:
    """Atomically deliver a message to an agent's inbox."""
    inbox = _inbox_dir(team, to)
    ts = int(time.time() * 1000)
    uid = uuid.uuid4().hex[:8]
    msg = {
        "type": msg_type,
        "from": from_agent,
        "to": to,
        "content": content,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    target = inbox / f"msg-{ts}-{uid}.json"
    tmp = inbox / f".tmp-{uid}.json"
    try:
        tmp.write_text(json.dumps(msg, indent=2), "utf-8")
        tmp.rename(target)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise


def _fetch(team: str, agent: str, consume: bool = True, limit: int = 20) -> list[dict]:
    """Fetch messages from an agent's inbox."""
    inbox = _inbox_dir(team, agent)
    files = sorted(inbox.glob("msg-*.json"))
    messages = []
    for f in files[:limit]:
        try:
            if consume:
                consumed = f.with_suffix(".consumed")
                try:
                    f.rename(consumed)
                except OSError:
                    continue
                try:
                    messages.append(json.loads(consumed.read_text("utf-8")))
                finally:
                    consumed.unlink(missing_ok=True)
            else:
                messages.append(json.loads(f.read_text("utf-8")))
        except Exception:
            continue
    return messages


def _list_agents(team: str) -> list[str]:
    """List all agents with inboxes."""
    inboxes_root = data_dir() / "teams" / team / "inboxes"
    if not inboxes_root.exists():
        return []
    return [d.name for d in inboxes_root.iterdir() if d.is_dir()]


@click.group("inbox")
def cmd_inbox() -> None:
    """Inter-agent messaging."""
    pass


@cmd_inbox.command("send")
@click.argument("team")
@click.argument("to")
@click.argument("message")
@click.option("--from", "from_agent", required=True, help="Sender agent name")
def inbox_send(team: str, to: str, message: str, from_agent: str) -> None:
    """Send a message to an agent."""
    _deliver(team, to, from_agent, message)
    click.echo(f"✉️  Sent to {to}")


@cmd_inbox.command("broadcast")
@click.argument("team")
@click.argument("message")
@click.option("--from", "from_agent", required=True, help="Sender agent name")
def inbox_broadcast(team: str, message: str, from_agent: str) -> None:
    """Broadcast a message to all agents."""
    agents = _list_agents(team)
    sent = 0
    for agent in agents:
        if agent != from_agent:
            _deliver(team, agent, from_agent, message, "broadcast")
            sent += 1
    click.echo(f"📢 Broadcast sent to {sent} agents")


@cmd_inbox.command("read")
@click.argument("team")
@click.argument("agent")
def inbox_read(team: str, agent: str) -> None:
    """Read and consume messages."""
    messages = _fetch(team, agent, consume=True)
    if not messages:
        click.echo("📭 No messages")
        return

    console = Console()
    for msg in messages:
        console.print(Panel(
            f"[bold]{msg.get('content', '')}[/bold]",
            title=f"From: {msg.get('from', '?')}",
            subtitle=msg.get("timestamp", ""),
        ))


@cmd_inbox.command("peek")
@click.argument("team")
@click.argument("agent")
def inbox_peek(team: str, agent: str) -> None:
    """Preview messages without consuming."""
    messages = _fetch(team, agent, consume=False)
    if not messages:
        click.echo("📭 No messages")
        return

    console = Console()
    for msg in messages:
        console.print(Panel(
            f"[bold]{msg.get('content', '')}[/bold]",
            title=f"From: {msg.get('from', '?')} [dim](unread)[/dim]",
            subtitle=msg.get("timestamp", ""),
        ))
