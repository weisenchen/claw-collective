"""octeam plan — approval workflows for team changes.

Innovation: simple state transitions (pending -> approved/rejected).
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from octeam.config import data_dir
from octeam.locking import atomic_write_json, file_lock


def _plan_dir(team: str) -> Path:
    d = data_dir() / "teams" / team / "plans"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _list_plans(team: str) -> list[dict]:
    d = _plan_dir(team)
    plans = []
    for f in sorted(d.glob("*.json")):
        try:
            plans.append(json.loads(f.read_text("utf-8")))
        except Exception:
            continue
    return plans


def _update_status(team: str, plan_id: str, status: str, reviewer: str = "Admin") -> bool:
    target = _plan_dir(team) / f"{plan_id}.json"
    if not target.exists():
        return False

    with file_lock(target.with_suffix(".lock")):
        try:
            plan = json.loads(target.read_text("utf-8"))
            plan["status"] = status
            plan["updated_at"] = datetime.now(timezone.utc).isoformat()
            plan["reviewer"] = reviewer
            atomic_write_json(target, plan)
            return True
        except Exception:
            return False


@click.group("plan")
def cmd_plan() -> None:
    """Approval workflows."""
    pass


@cmd_plan.command("submit")
@click.argument("team")
@click.argument("description")
@click.option("--author", required=True, help="Author agent name")
def plan_submit(team: str, description: str, author: str) -> None:
    """Submit a plan for approval."""
    plan_id = uuid.uuid4().hex[:8]
    plan = {
        "id": plan_id,
        "team": team,
        "description": description,
        "author": author,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    target = _plan_dir(team) / f"{plan_id}.json"
    atomic_write_json(target, plan)
    click.echo(f"📝 Plan '{plan_id}' submitted for team '{team}'")


@cmd_plan.command("list")
@click.argument("team")
def plan_list(team: str) -> None:
    """List plans for a team."""
    plans = _list_plans(team)
    if not plans:
        click.echo(f"No plans found for team '{team}'")
        return

    console = Console()
    table = Table(title=f"Plans for {team}")
    table.add_column("ID", style="cyan")
    table.add_column("Author")
    table.add_column("Description")
    table.add_column("Status")
    table.add_column("Date")

    for p in plans:
        status_style = "yellow" if p["status"] == "pending" else "green" if p["status"] == "approved" else "red"
        table.add_row(
            p["id"],
            p["author"],
            p["description"],
            f"[{status_style}]{p['status']}[/{status_style}]",
            p["created_at"][:10],
        )

    console.print(table)


@cmd_plan.command("approve")
@click.argument("team")
@click.argument("plan_id")
def plan_approve(team: str, plan_id: str) -> None:
    """Approve a pending plan."""
    if _update_status(team, plan_id, "approved"):
        click.echo(f"✅ Plan '{plan_id}' approved")
    else:
        click.echo(f"❌ Plan '{plan_id}' not found")


@cmd_plan.command("reject")
@click.argument("team")
@click.argument("plan_id")
def plan_reject(team: str, plan_id: str) -> None:
    """Reject a pending plan."""
    if _update_status(team, plan_id, "rejected"):
        click.echo(f"❌ Plan '{plan_id}' rejected")
    else:
        click.echo(f"❌ Plan '{plan_id}' not found")
