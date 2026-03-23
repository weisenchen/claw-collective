"""Claw Collective workspace — workspace management for git worktrees.

Innovation: simple CLI for listing and cleaning up git worktrees.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table


def _run_cmd(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


@click.group("ws")
def cmd_ws() -> None:
    """Workspace management."""
    pass


@cmd_ws.command("list")
def ws_list() -> None:
    """List all git worktrees."""
    res = _run_cmd(["git", "worktree", "list"])
    if res.returncode != 0:
        click.echo("❌ Not in a git repository or git worktree not supported")
        return

    console = Console()
    table = Table(title="Git Worktrees")
    table.add_column("Path", style="cyan")
    table.add_column("Commit")
    table.add_column("Branch")

    lines = res.stdout.strip().splitlines()
    for line in lines:
        parts = line.split()
        if len(parts) >= 3:
            table.add_row(parts[0], parts[1], parts[2])
        elif len(parts) == 2:
            table.add_row(parts[0], parts[1], "")
    
    console.print(table)


@cmd_ws.command("clean")
@click.option("--force", is_flag=True, help="Force cleanup")
def ws_clean(force: bool) -> None:
    """Clean up stale git worktrees."""
    click.echo("Cleaning up git worktrees...")
    res = _run_cmd(["git", "worktree", "prune"])
    if res.returncode == 0:
        click.echo("✅ Stale worktrees pruned")
    else:
        click.echo(f"❌ Failed to prune worktrees: {res.stderr.strip()}")

    # Also clean up octeam-worktrees dir if empty or specified
    worktree_parent = Path(os.getcwd()).parent / "octeam-worktrees"
    if worktree_parent.exists():
        if force:
            shutil.rmtree(worktree_parent)
            click.echo(f"🗑️  Deleted {worktree_parent}")
        else:
            # Only delete if empty
            try:
                worktree_parent.rmdir()
                click.echo(f"🗑️  Deleted empty {worktree_parent}")
            except OSError:
                click.echo(f"📍 {worktree_parent} is not empty. Use --force to delete.")


@cmd_ws.command("save")
@click.option("--message", "-m", help="Save message")
def ws_save(message: str | None) -> None:
    """Save changes (git commit) in current worktree."""
    current_dir = Path(os.getcwd())
    res = _run_cmd(["git", "rev-parse", "--is-inside-work-tree"], current_dir)
    if res.returncode != 0:
        click.echo("❌ Not in a git worktree")
        return

    from datetime import datetime
    msg = message or f"octeam checkpoint: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    _run_cmd(["git", "add", "."], current_dir)
    res = _run_cmd(["git", "commit", "-m", msg], current_dir)
    if res.returncode == 0:
        click.echo(f"✅ Changes saved: {msg}")
    else:
        click.echo(f"ℹ️  No changes to save or commit failed: {res.stdout.strip()}")


@cmd_ws.command("merge")
@click.argument("target", default="main")
def ws_merge(target: str) -> None:
    """Merge current worktree branch into target branch."""
    current_dir = Path(os.getcwd())
    # Get current branch
    res = _run_cmd(["git", "branch", "--show-current"], current_dir)
    current_branch = res.stdout.strip()
    if not current_branch:
        click.echo("❌ Could not determine current branch")
        return

    click.echo(f"Merging {current_branch} into {target}...")
    # This is a bit complex to do safely in a simple CLI, 
    # but we'll try the basic sequence.
    # Note: git checkout target in a worktree usually requires staying in the worktree
    # or using the main repo. This simplified version assumes we are in a worktree.
    res = _run_cmd(["git", "checkout", target], current_dir)
    if res.returncode != 0:
        click.echo(f"❌ Failed to checkout {target}: {res.stderr.strip()}")
        return

    res = _run_cmd(["git", "merge", current_branch], current_dir)
    if res.returncode == 0:
        click.echo(f"✅ Successfully merged {current_branch} into {target}")
    else:
        click.echo(f"❌ Merge failed: {res.stderr.strip()}")
