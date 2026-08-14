import click

from maxoa.generate import generate
from maxoa.merge import merge


@click.group()
def cli() -> None:
    """MAxO annotation pipeline."""


cli.add_command(generate)
cli.add_command(merge)
