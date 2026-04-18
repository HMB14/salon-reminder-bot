import click
from salon.commands.add import add_cmd
from salon.commands.list import list_cmd


@click.group()
def cli():
    """WhatsApp appointment reminder bot for beauty salons."""


cli.add_command(add_cmd)
cli.add_command(list_cmd)
