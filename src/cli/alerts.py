from datetime import date

import click
from rich.console import Console

from services.AlertService import AlertService

console = Console()


@click.command()
@click.option("--month", default=None, help="Month YYYY-MM (default: current month)")
@click.pass_context
def alerts(ctx: click.Context, month: str | None) -> None:
    """Show categories that exceeded their spending limit."""
    svc: AlertService = ctx.obj["alert_service"]
    month = month or date.today().strftime("%Y-%m")
    exceeded = svc.list_exceeded(month)

    if not exceeded:
        console.print(f"[green]No categories exceeded their limit in {month}.[/green]")
        return

    console.print(f"[bold red]Alerts — {month}[/bold red]")
    for msg in exceeded:
        console.print(f"  [red]•[/red] {msg}")
