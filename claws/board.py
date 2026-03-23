"""octeam board — terminal kanban dashboard.

Innovation: Rich-based terminal kanban instead of requiring a web browser.
"""

from __future__ import annotations

import time

import click
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

from octeam.task import TaskStatus, _list_all_tasks


def _build_kanban(team: str) -> Columns:
    """Build a Rich kanban board from task state."""
    tasks = _list_all_tasks(team)

    columns_data = {
        "📋 Pending": [],
        "▶️ In Progress": [],
        "🔒 Blocked": [],
        "✅ Completed": [],
    }

    status_map = {
        TaskStatus.PENDING: "📋 Pending",
        TaskStatus.IN_PROGRESS: "▶️ In Progress",
        TaskStatus.BLOCKED: "🔒 Blocked",
        TaskStatus.COMPLETED: "✅ Completed",
    }

    style_map = {
        TaskStatus.PENDING: "yellow",
        TaskStatus.IN_PROGRESS: "blue",
        TaskStatus.BLOCKED: "red",
        TaskStatus.COMPLETED: "green",
    }

    for t in tasks:
        col = status_map.get(t.status, "📋 Pending")
        style = style_map.get(t.status, "white")
        owner_str = f"\n[dim]{t.owner}[/dim]" if t.owner else ""
        columns_data[col].append(
            Panel(
                f"[{style}]{t.subject}[/{style}]{owner_str}",
                title=f"[dim]{t.id}[/dim]",
                width=30,
            )
        )

    panels = []
    for col_title, items in columns_data.items():
        if not items:
            items = [Panel("[dim]empty[/dim]", width=30)]
        table = Table(title=col_title, show_header=False, show_edge=False, pad_edge=False)
        table.add_column(width=32)
        for item in items:
            table.add_row(item)
        panels.append(table)

    return Columns(panels, equal=True, expand=True)


@click.group("board")
def cmd_board() -> None:
    """Terminal kanban dashboard."""
    pass


@cmd_board.command("show")
@click.argument("team")
def board_show(team: str) -> None:
    """Show kanban board in terminal."""
    console = Console()
    kanban = _build_kanban(team)
    console.print(kanban)


@cmd_board.command("live")
@click.argument("team")
@click.option("--interval", "-i", default=3, help="Refresh interval in seconds")
def board_live(team: str, interval: int) -> None:
    """Auto-refreshing kanban board."""
    console = Console()
    click.echo("Press Ctrl+C to stop")
    try:
        with Live(console=console, refresh_per_second=1) as live:
            while True:
                kanban = _build_kanban(team)
                live.update(kanban)
                time.sleep(interval)
    except KeyboardInterrupt:
        click.echo("\nStopped")
