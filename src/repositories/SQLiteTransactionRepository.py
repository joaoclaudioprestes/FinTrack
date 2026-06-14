import sqlite3
from dataclasses import replace

from models.Category import Category
from models.enums import TransactionType
from models.Transaction import Transaction
from repositories.TransactionRepository import TransactionRepository

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS transactions (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    amount           REAL    NOT NULL,
    date             TEXT    NOT NULL,
    type             TEXT    NOT NULL,
    category_name    TEXT    NOT NULL,
    category_limit   REAL    NOT NULL,
    description      TEXT    NOT NULL
)
"""


def _row_to_transaction(row: sqlite3.Row) -> Transaction:
    return Transaction(
        amount=row["amount"],
        date=row["date"],
        type=TransactionType(row["type"]),
        category=Category(name=row["category_name"], limit=row["category_limit"]),
        description=row["description"],
        id=row["id"],
    )


class SQLiteTransactionRepository(TransactionRepository):
    def __init__(self, db_path: str = "fintrack.db") -> None:
        self._db_path = db_path
        with self._connect() as conn:
            conn.execute(_CREATE_TABLE)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, transaction: Transaction) -> Transaction:
        sql = """
        INSERT INTO transactions (amount, date, type, category_name, category_limit, description)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        with self._connect() as conn:
            cursor = conn.execute(
                sql,
                (
                    transaction.amount,
                    transaction.date,
                    transaction.type,
                    transaction.category.name,
                    transaction.category.limit,
                    transaction.description,
                ),
            )
            return replace(transaction, id=cursor.lastrowid)

    def get_by_id(self, transaction_id: int) -> Transaction | None:
        row = (
            self._connect()
            .execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
            .fetchone()
        )
        return _row_to_transaction(row) if row else None

    def list_all(self) -> list[Transaction]:
        rows = self._connect().execute("SELECT * FROM transactions").fetchall()
        return [_row_to_transaction(r) for r in rows]

    def update(self, transaction: Transaction) -> Transaction:
        sql = """
        UPDATE transactions
        SET amount = ?, date = ?, type = ?, category_name = ?, category_limit = ?, description = ?
        WHERE id = ?
        """
        with self._connect() as conn:
            conn.execute(
                sql,
                (
                    transaction.amount,
                    transaction.date,
                    transaction.type,
                    transaction.category.name,
                    transaction.category.limit,
                    transaction.description,
                    transaction.id,
                ),
            )
        return transaction

    def delete(self, transaction_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
