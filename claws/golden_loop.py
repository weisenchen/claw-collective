"""Golden Loop — the core sync workflow for every shared-state operation.

Innovation over vendor: ClawTeam requires manual pull/push. octeam makes this
automatic via a context manager that wraps every command touching shared state.

The loop: PULL → LOCK → WORK → LOG → PUSH
"""

from __future__ import annotations

import subprocess
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run a git command in the given directory."""
    return subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def _is_git_repo(path: Path) -> bool:
    """Check if path is inside a git repo."""
    result = _git(["rev-parse", "--is-inside-work-tree"], path)
    return result.returncode == 0


def _has_remote(path: Path) -> bool:
    """Check if git repo has a remote configured."""
    result = _git(["remote"], path)
    return bool(result.stdout.strip())


@contextmanager
def golden_loop(
    workspace: Path,
    agent_id: str,
    task_desc: str,
    status_file: str = "STATUS.md",
    context_file: str = "memory/global_context.md",
    auto_push: bool = True,
) -> Generator[None, None, None]:
    """Context manager implementing the Golden Loop.

    Usage:
        with golden_loop(workspace, "Machine-A", "Creating API specs"):
            # do your work here
            ...
    """
    if not _is_git_repo(workspace):
        # Not a git repo — just execute without sync
        yield
        return

    has_remote = _has_remote(workspace)

    # 1. PULL
    if has_remote:
        _git(["pull", "--rebase"], workspace)

    # 2. LOCK — update STATUS.md
    status_path = workspace / status_file
    if status_path.exists():
        lines = status_path.read_text("utf-8").splitlines()
        updated = False
        new_lines = []
        for line in lines:
            if line.startswith(f"{agent_id}"):
                new_lines.append(f"{agent_id}: ACTIVE - {task_desc}")
                updated = True
            else:
                new_lines.append(line)
        if not updated:
            new_lines.append(f"{agent_id}: ACTIVE - {task_desc}")
        status_path.write_text("\n".join(new_lines) + "\n", "utf-8")

    try:
        # 3. WORK — caller does their work inside the context
        yield
    finally:
        # 4. LOG — append summary to global_context.md
        context_path = workspace / context_file
        if context_path.exists():
            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
            with open(context_path, "a", encoding="utf-8") as f:
                f.write(f"- {now}: [{agent_id}] {task_desc}\n")

        # Update status to IDLE
        if status_path.exists():
            lines = status_path.read_text("utf-8").splitlines()
            new_lines = []
            for line in lines:
                if line.startswith(f"{agent_id}"):
                    new_lines.append(f"{agent_id}: IDLE - Completed: {task_desc}")
                else:
                    new_lines.append(line)
            status_path.write_text("\n".join(new_lines) + "\n", "utf-8")

        # 5. PUSH
        if auto_push and has_remote:
            _git(["add", "."], workspace)
            _git(["commit", "-m", f"[{agent_id}] {task_desc}"], workspace)
            _git(["push"], workspace)
