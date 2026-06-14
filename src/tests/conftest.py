import pytest

from models.Category import Category
from models.enums import TransactionType
from models.Transaction import Transaction


@pytest.fixture
def category() -> Category:
    return Category(name="Food", limit=500.0)


@pytest.fixture
def transaction(category: Category) -> Transaction:
    return Transaction(
        amount=100.0,
        date="2026-06-01",
        type=TransactionType.EXPENSE,
        category=category,
        description="Lunch",
    )
