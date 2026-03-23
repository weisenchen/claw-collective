"""Claw Collective CLI — OpenClaw Team coordination tool.

A unified, simple CLI for multi-machine agent coordination.
"""

from __future__ import annotations

import click

from claws import __version__
from claws.a2a import cmd_a2a
from claws.board import cmd_board
from claws.config import cmd_config
from claws.dashboard import cmd_dashboard
from claws.inbox import cmd_inbox
from claws.init import cmd_init
from claws.lifecycle import cmd_idle, cmd_shutdown
from claws.plan import cmd_plan
from claws.register import cmd_register, cmd_unregister
from claws.spawn import cmd_spawn
from claws.sync import cmd_sync
from claws.task import cmd_task
from claws.team import cmd_team
from claws.template import cmd_launch
from claws.workspace_mgr import cmd_ws


@click.group()
@click.version_option(version=__version__, prog_name="claws")
def cli() -> None:
    """🦞 claws — Claw Collective CLI

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
