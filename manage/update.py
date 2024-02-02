"""Update commands."""

import click

from manage.utils import (
    run_subprocess,
)


@click.command(name="poetry")
def update_poetry():
    """Update Poetry installation.

    :return:
    """
    run_subprocess(["poetry", "self", "update"])
