import sqlite3

from models.Category import Category
from repositories.CategoryRepository import CategoryRepository

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS categories (
    name   TEXT PRIMARY KEY,
    limit_ REAL NOT NULL
)
"""


def _row_to_category(row: sqlite3.Row) -> Category:
    return Category(name=row["name"], limit=row["limit_"])


class SQLiteCategoryRepository(CategoryRepository):
    def __init__(self, db_path: str = "fintrack.db") -> None:
        self._db_path = db_path
        with self._connect() as conn:
            conn.execute(_CREATE_TABLE)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, category: Category) -> Category:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO categories (name, limit_) VALUES (?, ?)",
                (category.name, category.limit),
            )
        return category

    def get_by_name(self, name: str) -> Category | None:
        row = (
            self._connect()
            .execute("SELECT * FROM categories WHERE name = ?", (name,))
            .fetchone()
        )
        return _row_to_category(row) if row else None

    def list_all(self) -> list[Category]:
        rows = self._connect().execute("SELECT * FROM categories").fetchall()
        return [_row_to_category(r) for r in rows]

    def update(self, category: Category) -> Category:
        with self._connect() as conn:
            conn.execute(
                "UPDATE categories SET limit_ = ? WHERE name = ?",
                (category.limit, category.name),
            )
        return category

    def delete(self, name: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM categories WHERE name = ?", (name,))
