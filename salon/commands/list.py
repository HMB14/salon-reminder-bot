from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from salon.storage import load_appointments

console = Console()


@click.command("list")
@click.option("--last", "-l", default=20, show_default=True, help="Number of appointments to show")
def list_cmd(last):
    """List logged appointments (most recent first)."""
    appointments = load_appointments()
    if not appointments:
        console.print("[dim]No appointments logged yet.[/dim]")
        return

    recent = list(reversed(appointments))[:last]

    table = Table(title="Appointments", show_lines=True)
    table.add_column("Client", style="bold")
    table.add_column("Service")
    table.add_column("Date & Time")
    table.add_column("Phone")
    table.add_column("Branch")
    table.add_column("Stylist")

    for appt in recent:
        table.add_row(
            appt.name,
            appt.service,
            appt.time.strftime("%Y-%m-%d %H:%M"),
            appt.phone,
            appt.branch or "—",
            appt.stylist or "—",
        )

    console.print(table)
