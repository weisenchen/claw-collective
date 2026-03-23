"""Configuration management for octeam.

State lives in ~/.octeam/ (unified).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from pydantic import BaseModel


class OcteamConfig(BaseModel):
    """Global octeam configuration."""
    data_dir: str = ""
    workspace_dir: str = ""
    sync_remote: str = ""
    default_team: str = ""
    transport: str = "file"
    a2a_port: int = 18800
    a2a_token: str = ""


def data_dir() -> Path:
    """Return the octeam data directory (~/.octeam/)."""
    custom = os.environ.get("OCTEAM_DATA_DIR", "")
    p = Path(custom) if custom else Path.home() / ".octeam"
    p.mkdir(parents=True, exist_ok=True)
    return p


def config_path() -> Path:
    return data_dir() / "config.json"


def load_config() -> OcteamConfig:
    """Load config from disk. Returns defaults if missing."""
    p = config_path()
    if not p.exists():
        return OcteamConfig()
    try:
        return OcteamConfig.model_validate(json.loads(p.read_text("utf-8")))
    except Exception:
        return OcteamConfig()


def save_config(cfg: OcteamConfig) -> None:
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
