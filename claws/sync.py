"""octeam sync — git sync with secret scanning.

Innovation: inline secret scanning, Golden Loop integration, single module.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import click

from octeam.secrets import scan_and_report


def _git(args: list[str], cwd: Path, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)


def _find_workspace() -> Path:
    p = Path.cwd()
    for _ in range(10):
        if (p / "STATUS.md").exists():
            return p
        if p.parent == p:
            break
        p = p.parent
    return Path.cwd()


@click.group("sync")
def cmd_sync() -> None:
    """Git sync with secret scanning."""
    pass


@cmd_sync.command("push")
@click.option("--workspace", "-w", default="", help="Workspace path")
@click.option("--message", "-m", default="", help="Commit message")
@click.option("--auto", is_flag=True, help="Non-interactive mode for cron jobs")
def sync_push(workspace: str, message: str, auto: bool) -> None:
    """Scan for secrets, commit, and push to remote."""
    ws = Path(workspace) if workspace else _find_workspace()

    # Secret scan first
    click.echo("🔍 Scanning for secrets...")
    exit_code = scan_and_report(ws)
    if exit_code == 3:
        click.echo("❌ Push blocked: secrets detected. Remove them first.")
        raise SystemExit(3)

    # Stage and commit
    _git(["add", "."], ws)

    # Check if there are changes
    result = _git(["status", "--porcelain"], ws)
    if not result.stdout.strip():
        click.echo("ℹ️  No changes to push")
        return

    msg = message or "octeam sync push"
    _git(["commit", "-m", msg], ws)

    # Push
    result = _git(["push"], ws)
    if result.returncode != 0:
        click.echo(f"⚠️  Push failed: {result.stderr.strip()}")
        click.echo("Try: octeam sync pull first, then push again")
        raise SystemExit(1)

    click.echo("✅ Pushed successfully")


@cmd_sync.command("pull")
@click.option("--workspace", "-w", default="", help="Workspace path")
@click.option("--dry-run", is_flag=True, help="Preview changes without applying")
def sync_pull(workspace: str, dry_run: bool) -> None:
    """Pull remote changes into workspace."""
    ws = Path(workspace) if workspace else _find_workspace()

    if dry_run:
        _git(["fetch"], ws)
        result = _git(["diff", "HEAD", "FETCH_HEAD", "--stat"], ws)
        click.echo(result.stdout or "No changes")
        return

    if not click.confirm("⚠️  Pull can overwrite local files. Continue?"):
        return

    result = _git(["pull", "--rebase"], ws)
    if result.returncode == 0:
        click.echo("✅ Pulled successfully")
    else:
        click.echo(f"⚠️  Pull failed: {result.stderr.strip()}")


@cmd_sync.command("status")
@click.option("--workspace", "-w", default="", help="Workspace path")
def sync_status(workspace: str) -> None:
    """Show sync state."""
    ws = Path(workspace) if workspace else _find_workspace()

    # Local status
    result = _git(["status", "--short"], ws)
    if result.stdout.strip():
        click.echo("📝 Local changes:")
        click.echo(result.stdout)
    else:
        click.echo("✅ Working tree clean")

    # Remote status
    _git(["fetch"], ws)
    result = _git(["rev-list", "HEAD..@{u}", "--count"], ws)
    behind = result.stdout.strip()
    result = _git(["rev-list", "@{u}..HEAD", "--count"], ws)
    ahead = result.stdout.strip()

    if behind and behind != "0":
        click.echo(f"⬇️  {behind} commits behind remote")
    if ahead and ahead != "0":
        click.echo(f"⬆️  {ahead} commits ahead of remote")
    if (not behind or behind == "0") and (not ahead or ahead == "0"):
        click.echo("🔄 In sync with remote")
