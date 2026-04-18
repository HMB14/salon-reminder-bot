from __future__ import annotations
from datetime import datetime

import click
from rich.console import Console
from rich.rule import Rule

from salon.models import Appointment
from salon.storage import append_appointment
from salon.message import generate_messages

console = Console()


@click.command("add")
@click.option("--name", "-n", required=True, help="Client name")
@click.option("--service", "-s", required=True, help="Service (e.g. Haircut)")
@click.option("--time", "-t", "appt_time", required=True, help="Appointment time: YYYY-MM-DD HH:MM")
@click.option("--phone", "-p", required=True, help="WhatsApp number (e.g. +966501234567)")
@click.option("--stylist", help="Stylist name")
@click.option("--branch", help="Salon branch / location")
@click.option("--notes", help="Special requests or notes")
def add_cmd(name, service, appt_time, phone, stylist, branch, notes):
    """Log an appointment and print bilingual WhatsApp reminder."""
    try:
        parsed_time = datetime.strptime(appt_time, "%Y-%m-%d %H:%M")
    except ValueError:
        raise click.BadParameter("Use format YYYY-MM-DD HH:MM", param_hint="--time")

    appt = Appointment(
        name=name,
        service=service,
        time=parsed_time,
        phone=phone,
        stylist=stylist,
        branch=branch,
        notes=notes,
    )

    append_appointment(appt)

    en_msg, ar_msg = generate_messages(appt)

    console.print(Rule("[bold green]English Message[/bold green]"))
    console.print(en_msg)
    console.print()
    console.print(Rule("[bold blue]Arabic Message / الرسالة بالعربي[/bold blue]"))
    console.print(ar_msg)
    console.print()
    console.print(Rule())
    console.print(f"[dim]Send to:[/dim] [bold]{phone}[/bold]")
    console.print("[dim]Appointment logged.[/dim]")
