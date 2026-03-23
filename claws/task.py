"""octeam task — kanban task management with dependency tracking.

Innovation: simpler commands (task add/done vs task create/update --status),
unified ~/.octeam/ state.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import click
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

from octeam.config import data_dir
from octeam.locking import atomic_write_json, file_lock, read_json


class TaskStatus:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class TaskItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    subject: str
    status: str = TaskStatus.PENDING
    owner: str = ""
    blocked_by: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def _tasks_dir(team: str) -> Path:
    d = data_dir() / "teams" / team / "tasks"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _lock_path(team: str) -> Path:
    return data_dir() / "teams" / team / "tasks.lock"


def _save_task(team: str, task: TaskItem) -> None:
    path = _tasks_dir(team) / f"task-{task.id}.json"
    atomic_write_json(path, task.model_dump())


def _load_task(team: str, task_id: str) -> Optional[TaskItem]:
    path = _tasks_dir(team) / f"task-{task_id}.json"
    if not path.exists():
        return None
    data = read_json(path)
    return TaskItem.model_validate(data) if data else None


def _list_all_tasks(team: str) -> list[TaskItem]:
    tasks_path = _tasks_dir(team)
    tasks = []
    for f in sorted(tasks_path.glob("task-*.json")):
        try:
            data = json.loads(f.read_text("utf-8"))
            tasks.append(TaskItem.model_validate(data))
        except Exception:
            continue
    return tasks


def _unblock_dependents(team: str, completed_id: str) -> None:
    """Auto-unblock tasks that were waiting on the completed task."""
    for task in _list_all_tasks(team):
        if completed_id in task.blocked_by:
            task.blocked_by.remove(completed_id)
            if not task.blocked_by and task.status == TaskStatus.BLOCKED:
                task.status = TaskStatus.PENDING
            task.updated_at = datetime.now(timezone.utc).isoformat()
            _save_task(team, task)


@click.group("task")
def cmd_task() -> None:
    """Task management (kanban-style)."""
    pass


@cmd_task.command("add")
@click.argument("team")
@click.argument("subject")
@click.option("--owner", "-o", default="", help="Assign to an agent")
@click.option("--blocked-by", "-b", default="", help="Comma-separated task IDs this depends on")
def task_add(team: str, subject: str, owner: str, blocked_by: str) -> None:
    """Add a new task."""
    deps = [x.strip() for x in blocked_by.split(",") if x.strip()] if blocked_by else []
    status = TaskStatus.BLOCKED if deps else TaskStatus.PENDING
    task = TaskItem(subject=subject, owner=owner, blocked_by=deps, status=status)

    with file_lock(_lock_path(team)):
        _save_task(team, task)

    click.echo(f"✅ Created task {task.id}: {subject}")


@cmd_task.command("done")
@click.argument("team")
@click.argument("task_id")
def task_done(team: str, task_id: str) -> None:
    """Mark a task as completed."""
    with file_lock(_lock_path(team)):
        task = _load_task(team, task_id)
        if not task:
            click.echo(f"❌ Task {task_id} not found")
            return
        task.status = TaskStatus.COMPLETED
        task.updated_at = datetime.now(timezone.utc).isoformat()
        _save_task(team, task)
        _unblock_dependents(team, task_id)

    click.echo(f"✅ Task {task_id} completed")


@cmd_task.command("list")
@click.argument("team")
@click.option("--status", "-s", default="", help="Filter by status")
@click.option("--owner", "-o", default="", help="Filter by owner")
def task_list(team: str, status: str, owner: str) -> None:
    """List tasks (terminal kanban view)."""
    tasks = _list_all_tasks(team)

    if status:
        tasks = [t for t in tasks if t.status == status]
    if owner:
        tasks = [t for t in tasks if t.owner == owner]

    if not tasks:
        click.echo("No tasks found")
        return

    console = Console()
    table = Table(title=f"Tasks: {team}")
    table.add_column("ID", style="cyan", width=10)
    table.add_column("Status", width=12)
    table.add_column("Owner", width=15)
    table.add_column("Subject")

    status_styles = {
        TaskStatus.PENDING: "yellow",
        TaskStatus.IN_PROGRESS: "blue",
        TaskStatus.COMPLETED: "green",
        TaskStatus.BLOCKED: "red",
    }

    for t in tasks:
        style = status_styles.get(t.status, "white")
        table.add_row(t.id, f"[{style}]{t.status}[/{style}]", t.owner, t.subject)

    console.print(table)


@cmd_task.command("start")
@click.argument("team")
@click.argument("task_id")
@click.option("--owner", "-o", default="", help="Agent taking the task")
def task_start(team: str, task_id: str, owner: str) -> None:
    """Move a task to in_progress."""
    with file_lock(_lock_path(team)):
        task = _load_task(team, task_id)
        if not task:
            click.echo(f"❌ Task {task_id} not found")
            return
        task.status = TaskStatus.IN_PROGRESS
        if owner:
            task.owner = owner
        task.updated_at = datetime.now(timezone.utc).isoformat()
        _save_task(team, task)

    click.echo(f"▶️  Task {task_id} in progress" + (f" (owner: {owner})" if owner else ""))
