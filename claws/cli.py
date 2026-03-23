"""Claw Collective CLI — OpenClaw Team coordination tool.

A unified, simple CLI for multi-machine agent coordination.
"""

from __future__ import annotations

import click

from octeam import __version__
from octeam.a2a import cmd_a2a
from octeam.board import cmd_board
from octeam.config import cmd_config
from octeam.dashboard import cmd_dashboard
from octeam.inbox import cmd_inbox
from octeam.init import cmd_init
from octeam.lifecycle import cmd_idle, cmd_shutdown
from octeam.plan import cmd_plan
from octeam.register import cmd_register, cmd_unregister
from octeam.spawn import cmd_spawn
from octeam.sync import cmd_sync
from octeam.task import cmd_task
from octeam.team import cmd_team
from octeam.template import cmd_launch
from octeam.workspace_mgr import cmd_ws


@click.group()
@click.version_option(version=__version__, prog_name="octeam")
def cli() -> None:
    """🦞 octeam — OpenClaw Team CLI

    Multi-machine agent coordination made simple.
    """
    pass


# Register all subcommands
cli.add_command(cmd_init)
cli.add_command(cmd_register)
cli.add_command(cmd_unregister)
cli.add_command(cmd_sync)
cli.add_command(cmd_team)
cli.add_command(cmd_task)
cli.add_command(cmd_inbox)
cli.add_command(cmd_board)
cli.add_command(cmd_spawn)
cli.add_command(cmd_ws)
cli.add_command(cmd_plan)
cli.add_command(cmd_shutdown)
cli.add_command(cmd_idle)
cli.add_command(cmd_launch)
cli.add_command(cmd_a2a)
cli.add_command(cmd_dashboard)
cli.add_command(cmd_config)


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
