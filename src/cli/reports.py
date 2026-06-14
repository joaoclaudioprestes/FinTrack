import click
from rich.console import Console
from rich.table import Table

from services.ReportService import ReportService

console = Console()


@click.command()
@click.option("--month", required=True, help="Report month YYYY-MM")
@click.option("--csv", "as_csv", is_flag=True, default=False, help="Export as CSV")
@click.pass_context
def report(ctx: click.Context, month: str, as_csv: bool) -> None:
    """Generate a monthly report."""
    svc: ReportService = ctx.obj["report_service"]
    r = svc.generate_monthly(month)

    if as_csv:
        console.print("month,total_income,total_expense,net_balance")
        console.print(f"{r.month},{r.total_income},{r.total_expense},{r.net_balance}")
        return

    table = Table(title=f"Report — {r.month}", show_header=True, header_style="bold")
    table.add_column("Field", style="dim")
    table.add_column("Amount", justify="right")
    table.add_row("Income", f"[green]R$ {r.total_income:,.2f}[/green]")
    table.add_row("Expenses", f"[red]R$ {r.total_expense:,.2f}[/red]")
    color = "green" if r.net_balance >= 0 else "red"
    table.add_row("Balance", f"[{color}]R$ {r.net_balance:,.2f}[/{color}]")
    console.print(table)
