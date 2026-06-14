import os
import shlex
import sys
import termios
import tty

import click
from rich.console import Console
from rich.text import Text

from cli.transactions import add, edit, list_, remove
from cli.reports import report
from cli.alerts import alerts
from repositories.SQLiteTransactionRepository import SQLiteTransactionRepository
from services.AlertService import AlertService
from services.ReportService import ReportService
from services.TransactionService import TransactionService

_DEFAULT_DB = os.path.expanduser("~/.fintrack/fintrack.db")

_BANNER = """\
███████╗██╗███╗   ██╗████████╗██████╗  █████╗  ██████╗██╗  ██╗
██╔════╝██║████╗  ██║╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
█████╗  ██║██╔██╗ ██║   ██║   ██████╔╝███████║██║     █████╔╝
██╔══╝  ██║██║╚██╗██║   ██║   ██╔══██╗██╔══██║██║     ██╔═██╗
██║     ██║██║ ╚████║   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗
╚═╝     ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝\
"""

_COMMANDS = [
    ("add", "add a transaction"),
    ("list", "list transactions  --month  --category  --type"),
    ("edit", "edit a transaction  ID"),
    ("remove", "remove a transaction  ID"),
    ("report", "monthly report  --month  [--csv]"),
    ("alerts", "spending limit alerts  [--month]"),
    ("clear", "clear the terminal"),
    ("exit", "exit the application"),
]


def _print_welcome(console: Console) -> None:
    console.print(Text(_BANNER, style="bold green"))
    console.print()
    console.print("  [dim]personal finance tracker · SQLite · Python 3.12+[/dim]")
    console.print()
    console.print("  [bold]commands[/bold]")
    console.print()
    for cmd, desc in _COMMANDS:
        console.print(f"    [green]fintrack {cmd:<8}[/green]  [dim]{desc}[/dim]")
    console.print()
    console.print("  [dim]ESC to quit · <command> --help for details[/dim]")
    console.print()


def _read_line(prompt: str) -> str | None:
    """Reads a line of input. Returns None if ESC is pressed."""
    sys.stdout.write(prompt)
    sys.stdout.flush()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    chars: list[str] = []

    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch == "\x1b":  # ESC
                sys.stdout.write("\n")
                return None
            elif ch in ("\r", "\n"):  # Enter
                sys.stdout.write("\n")
                return "".join(chars)
            elif ch == "\x7f":  # Backspace
                if chars:
                    chars.pop()
                    sys.stdout.write("\b \b")
            elif ch == "\x03":  # Ctrl+C
                sys.stdout.write("\n")
                raise KeyboardInterrupt
            elif ch >= " ":
                chars.append(ch)
                sys.stdout.write(ch)
            sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def _run_repl(db: str) -> None:
    console = Console()
    _print_welcome(console)

    while True:
        try:
            line = _read_line("\033[32mfintrack\033[0m \033[2m›\033[0m ")
        except KeyboardInterrupt:
            break

        if line is None:
            break

        line = line.strip()
        if not line or line in ("exit", "quit"):
            break

        if line == "clear":
            sys.stdout.write("\033[2J\033[H")
            sys.stdout.flush()
            _print_welcome(console)
            continue

        args = shlex.split(line)
        if args and args[0] == "fintrack":
            args = args[1:]

        if not args:
            continue

        try:
            cli.main(
                ["--db", db] + args, standalone_mode=True, obj={}, prog_name="fintrack"
            )
        except SystemExit:
            pass
        except Exception as e:
            console.print(f"[red]error: {e}[/red]")

        console.print()


@click.group(invoke_without_command=True)
@click.option("--db", default=_DEFAULT_DB, hidden=True, envvar="FINTRACK_DB")
@click.pass_context
def cli(ctx: click.Context, db: str) -> None:
    """FinTrack — personal finance tracker."""
    os.makedirs(os.path.dirname(db), exist_ok=True)
    repo = SQLiteTransactionRepository(db)
    alert_svc = AlertService(repo)
    ctx.ensure_object(dict)
    ctx.obj["service"] = TransactionService(repo, alert_svc)
    ctx.obj["alert_service"] = alert_svc
    ctx.obj["report_service"] = ReportService(repo)

    if ctx.invoked_subcommand is None:
        _run_repl(db)


cli.add_command(add)
cli.add_command(list_)
cli.add_command(edit)
cli.add_command(remove)
cli.add_command(report)
cli.add_command(alerts)
