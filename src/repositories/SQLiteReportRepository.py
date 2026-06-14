import sqlite3

from models.Report import Report
from repositories.ReportRepository import ReportRepository

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS reports (
    month          TEXT PRIMARY KEY,
    total_income   REAL NOT NULL,
    total_expense  REAL NOT NULL,
    net_balance    REAL NOT NULL
)
"""


def _row_to_report(row: sqlite3.Row) -> Report:
    return Report(
        month=row["month"],
        total_income=row["total_income"],
        total_expense=row["total_expense"],
        net_balance=row["net_balance"],
    )


class SQLiteReportRepository(ReportRepository):
    def __init__(self, db_path: str = "fintrack.db") -> None:
        self._db_path = db_path
        with self._connect() as conn:
            conn.execute(_CREATE_TABLE)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def save(self, report: Report) -> Report:
        sql = """
        INSERT INTO reports (month, total_income, total_expense, net_balance)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(month) DO UPDATE SET
            total_income  = excluded.total_income,
            total_expense = excluded.total_expense,
            net_balance   = excluded.net_balance
        """
        with self._connect() as conn:
            conn.execute(
                sql,
                (
                    report.month,
                    report.total_income,
                    report.total_expense,
                    report.net_balance,
                ),
            )
        return report

    def get_by_month(self, month: str) -> Report | None:
        row = (
            self._connect()
            .execute("SELECT * FROM reports WHERE month = ?", (month,))
            .fetchone()
        )
        return _row_to_report(row) if row else None

    def list_all(self) -> list[Report]:
        rows = (
            self._connect().execute("SELECT * FROM reports ORDER BY month").fetchall()
        )
        return [_row_to_report(r) for r in rows]

    def delete(self, month: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM reports WHERE month = ?", (month,))
