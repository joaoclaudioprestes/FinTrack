from datetime import date

import click
from rich.console import Console
from rich.table import Table

from models.Category import Category
from models.enums import TransactionType
from models.Transaction import Transaction
from services.TransactionService import TransactionService

console = Console()


def _service(ctx: click.Context) -> TransactionService:
    return ctx.obj["service"]


@click.command()
@click.option("--amount", required=True, type=float, help="Transaction amount")
@click.option("--date", "date_", default=None, help="Date YYYY-MM-DD (default: today)")
@click.option(
    "--type",
    "type_",
    required=True,
    type=click.Choice(["income", "expense"]),
    help="Transaction type",
)
@click.option("--category", required=True, help="Category name")
@click.option(
    "--category-limit",
    default=0.0,
    type=float,
    show_default=True,
    help="Monthly category limit",
)
@click.option("--description", required=True, help="Description")
@click.pass_context
def add(
    ctx: click.Context,
    amount: float,
    date_: str | None,
    type_: str,
    category: str,
    category_limit: float,
    description: str,
) -> None:
    """Add a transaction."""
    transaction = Transaction(
        amount=amount,
        date=date_ or date.today().isoformat(),
        type=TransactionType(type_),
        category=Category(name=category, limit=category_limit),
        description=description,
    )
    saved = _service(ctx).create(transaction)
    console.print(f"[green]Transaction #{saved.id} created.[/green]")


@click.command(name="list")
@click.option("--month", default=None, help="Filter by month YYYY-MM")
@click.option("--category", default=None, help="Filter by category")
@click.option(
    "--type",
    "type_",
    default=None,
    type=click.Choice(["income", "expense"]),
    help="Filter by type",
)
@click.pass_context
def list_(
    ctx: click.Context, month: str | None, category: str | None, type_: str | None
) -> None:
    """List transactions."""
    transactions = _service(ctx).list_all()

    if month:
        transactions = [t for t in transactions if t.date.startswith(month)]
    if category:
        transactions = [
            t for t in transactions if t.category.name.lower() == category.lower()
        ]
    if type_:
        transactions = [t for t in transactions if t.type == TransactionType(type_)]

    if not transactions:
        console.print("[yellow]No transactions found.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Date")
    table.add_column("Type")
    table.add_column("Amount", justify="right")
    table.add_column("Category")
    table.add_column("Description")

    for t in transactions:
        color = "green" if t.type == TransactionType.INCOME else "red"
        table.add_row(
            str(t.id),
            t.date,
            f"[{color}]{t.type}[/{color}]",
            f"[{color}]R$ {t.amount:,.2f}[/{color}]",
            t.category.name,
            t.description,
        )

    console.print(table)


@click.command()
@click.argument("id", type=int)
@click.option("--amount", default=None, type=float, help="New amount")
@click.option("--date", "date_", default=None, help="New date YYYY-MM-DD")
@click.option(
    "--type",
    "type_",
    default=None,
    type=click.Choice(["income", "expense"]),
    help="New type",
)
@click.option("--category", default=None, help="New category")
@click.option(
    "--category-limit", default=None, type=float, help="New category limit"
)
@click.option("--description", default=None, help="New description")
@click.pass_context
def edit(
    ctx: click.Context,
    id: int,
    amount: float | None,
    date_: str | None,
    type_: str | None,
    category: str | None,
    category_limit: float | None,
    description: str | None,
) -> None:
    """Edit an existing transaction."""
    service = _service(ctx)
    existing = service.get(id)

    if existing is None:
        console.print(f"[red]Transaction #{id} not found.[/red]")
        raise SystemExit(1)

    updated = Transaction(
        amount=amount if amount is not None else existing.amount,
        date=date_ or existing.date,
        type=TransactionType(type_) if type_ else existing.type,
        category=Category(
            name=category or existing.category.name,
            limit=category_limit
            if category_limit is not None
            else existing.category.limit,
        ),
        description=description or existing.description,
        id=existing.id,
    )
    service.update(updated)
    console.print(f"[green]Transaction #{id} updated.[/green]")


@click.command()
@click.argument("id", type=int)
@click.confirmation_option(prompt="Are you sure you want to remove this transaction?")
@click.pass_context
def remove(ctx: click.Context, id: int) -> None:
    """Remove a transaction."""
    service = _service(ctx)

    if service.get(id) is None:
        console.print(f"[red]Transaction #{id} not found.[/red]")
        raise SystemExit(1)

    service.delete(id)
    console.print(f"[green]Transaction #{id} removed.[/green]")
