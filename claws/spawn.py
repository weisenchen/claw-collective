"""Claw Collective spawn — agent spawning and isolation.

Innovation: unified command, auto-detects path, supports tmux + worktree.
"""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import time
from pathlib import Path

import click

from claws.config import load_config


def _is_tmux_available() -> bool:
    return bool(shutil.which("tmux"))


def _run_cmd(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )


@click.command("spawn")
@click.option("--team", "-t", required=True, help="Team name")
@click.option("--name", "-n", required=True, help="Agent name")
@click.option("--task", "-m", required=True, help="Task description")
@click.option("--no-tmux", is_flag=True, help="Don't use tmux")
@click.option("--no-worktree", is_flag=True, help="Don't use git worktree")
@click.argument("command", nargs=-1)
def cmd_spawn(team: str, name: str, task: str, no_tmux: bool, no_worktree: bool, command: tuple[str, ...]) -> None:
    """Spawn an agent for a specific task.

    If no command is provided, it defaults to 'claude-code' if available, or 'bash'.
    """
    config = load_config()
    workspace_root = Path(config.workspace_dir or os.getcwd())

    # 1. Isolation: Git Worktree (if requested and possible)
    spawn_cwd = workspace_root
    if not no_worktree:
        git_check = _run_cmd(["git", "rev-parse", "--is-inside-work-tree"], workspace_root)
        if git_check.returncode == 0:
            worktree_dir = workspace_root.parent / f"claws-worktrees" / f"{team}-{name}"
            worktree_dir.parent.mkdir(parents=True, exist_ok=True)
            if not worktree_dir.exists():
                click.echo(f"Creating git worktree at {worktree_dir}...")
                res = _run_cmd(["git", "worktree", "add", str(worktree_dir), "HEAD"], workspace_root)
                if res.returncode != 0:
                    click.echo(f"⚠️  Failed to create worktree: {res.stderr.strip()}. Falling back to main workspace.")
                else:
                    spawn_cwd = worktree_dir
            else:
                spawn_cwd = worktree_dir

    # 2. Determine command
    if not command:
        if shutil.which("claude-code"):
            command = ("claude-code",)
        elif shutil.which("claude"):
            command = ("claude",)
        else:
            command = ("bash",)

    cmd_str = " ".join(shlex.quote(c) for c in command)

    # 3. Execution: Tmux or Subprocess
    if not no_tmux and _is_tmux_available():
        session_name = f"claws-{team}"
        window_name = name

        # Check if session exists
        check = _run_cmd(["tmux", "has-session", "-t", session_name])

        env_vars = {
            "CLAWS_TEAM": team,
            "CLAWS_AGENT": name,
            "CLAWS_TASK": task,
        }
        export_str = "; ".join(f"export {k}={shlex.quote(v)}" for k, v in env_vars.items())
        full_command = f"{export_str}; cd {shlex.quote(str(spawn_cwd))} && {cmd_str}"

        if check.returncode != 0:
            # Create session
            _run_cmd(["tmux", "new-session", "-d", "-s", session_name, "-n", window_name, full_command])
        else:
            # Create new window in existing session
            _run_cmd(["tmux", "new-window", "-t", session_name, "-n", window_name, full_command])

        click.echo(f"🚀 Started agent '{name}' in tmux session '{session_name}:{window_name}'")
        click.echo(f"📍 Directory: {spawn_cwd}")
        click.echo(f"📝 Task: {task}")
    else:
        # Fallback to subprocess (blocking)
        click.echo(f"🚀 Starting agent '{name}' (non-tmux)...")
        env = os.environ.copy()
        env["CLAWS_TEAM"] = team
        env["CLAWS_AGENT"] = name
        env["CLAWS_TASK"] = task

        subprocess.run(command, cwd=spawn_cwd, env=env)
