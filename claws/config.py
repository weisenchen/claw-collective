"""Configuration management for Claw Collective.

State lives in ~/.claws/ (unified).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from pydantic import BaseModel


class ClawsConfig(BaseModel):
    """Global Claw Collective configuration."""
    data_dir: str = ""
    workspace_dir: str = ""
    sync_remote: str = ""
    default_team: str = ""
    transport: str = "file"
    a2a_port: int = 18800
    a2a_token: str = ""


def data_dir() -> Path:
    """Return the Claw Collective data directory.
    
    Order of preference:
    1. CLAWS_DATA_DIR env var
    2. .openclaw/ directory in current or parent hierarchy
    3. ~/.claws/ (fallback)
    """
    custom = os.environ.get("CLAWS_DATA_DIR", "")
    if custom:
        p = Path(custom)
    else:
        # Search for .openclaw/ up the directory tree
        found_dir = None
        current = Path.cwd().resolve()
        for _ in range(10): # Max depth 10
            target = current / ".openclaw"
            if target.is_dir():
                found_dir = target
                break
            if current.parent == current:
                break
            current = current.parent
        
        p = found_dir if found_dir else Path.home() / ".claws"
    
    p.mkdir(parents=True, exist_ok=True)
    return p


def config_path() -> Path:
    return data_dir() / "config.json"


def load_config() -> ClawsConfig:
    """Load config from disk. Returns defaults if missing."""
    p = config_path()
    if not p.exists():
        return ClawsConfig()
    try:
        return ClawsConfig.model_validate(json.loads(p.read_text("utf-8")))
    except Exception:
        return ClawsConfig()


def save_config(cfg: ClawsConfig) -> None:
    """Atomically write config."""
    p = config_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(cfg.model_dump_json(indent=2), encoding="utf-8")
    tmp.rename(p)


import click
from rich.console import Console

@click.group("config")
def cmd_config() -> None:
    """Configuration management."""
    pass


@cmd_config.command("show")
def config_show() -> None:
    """Show current configuration."""
    cfg = load_config()
    console = Console()
    console.print(cfg.model_dump_json(indent=2))


@cmd_config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str) -> None:
    """Set a configuration value."""
    cfg = load_config()
    if not hasattr(cfg, key):
        click.echo(f"❌ Unknown config key: {key}")
        return
    
    # Simple type conversion
    current = getattr(cfg, key)
    try:
        if isinstance(current, int):
            setattr(cfg, key, int(value))
        else:
            setattr(cfg, key, value)
        save_config(cfg)
        click.echo(f"✅ Set {key} = {value}")
    except ValueError:
        click.echo(f"❌ Invalid value for {key}: {value} (expected {type(current).__name__})")


@cmd_config.command("health")
def config_health() -> None:
    """Check system health and directory status."""
    d = data_dir()
    click.echo(f"📍 Data directory: {d}")
    click.echo(f"📂 Exists: {d.exists()}")
    
    config = load_config()
    click.echo(f"⚙️  Workspace: {config.workspace_dir or 'Not set'}")
    
    # Check git
    git_res = subprocess.run(["git", "--version"], capture_output=True, text=True)
    click.echo(f"🛠️  Git: {git_res.stdout.strip() if git_res.returncode == 0 else 'Not found'}")
    
    # Check tmux
    tmux_res = subprocess.run(["tmux", "-V"], capture_output=True, text=True)
    click.echo(f"🖥️  Tmux: {tmux_res.stdout.strip() if tmux_res.returncode == 0 else 'Not found'}")
