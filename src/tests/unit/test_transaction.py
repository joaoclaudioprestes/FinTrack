import pytest

from models.Category import Category
from models.enums import TransactionType
from models.Transaction import Transaction


@pytest.fixture
def category():
    return Category(name="Food", limit=500.0)


def test_valid_transaction(category):
    t = Transaction(
        amount=50.0,
        date="2026-06-01",
        type=TransactionType.EXPENSE,
        category=category,
        description="Lunch",
    )
    assert t.id is None
    assert t.amount == 50.0


def test_id_defaults_to_none(category):
    t = Transaction(
        amount=10.0,
        date="2026-06-01",
        type=TransactionType.INCOME,
        category=category,
        description="Tip",
    )
    assert t.id is None


def test_zero_amount_raises(category):
    with pytest.raises(ValueError, match="greater than zero"):
        Transaction(
            amount=0.0,
            date="2026-06-01",
            type=TransactionType.EXPENSE,
            category=category,
            description="x",
        )


def test_negative_amount_raises(category):
    with pytest.raises(ValueError, match="greater than zero"):
        Transaction(
            amount=-50.0,
            date="2026-06-01",
            type=TransactionType.EXPENSE,
            category=category,
            description="x",
        )


def test_empty_date_raises(category):
    with pytest.raises(ValueError, match="Date cannot be empty"):
        Transaction(
            amount=10.0,
            date="",
            type=TransactionType.EXPENSE,
            category=category,
            description="x",
        )


def test_empty_description_raises(category):
    with pytest.raises(ValueError, match="Description cannot be empty"):
        Transaction(
            amount=10.0,
            date="2026-06-01",
            type=TransactionType.EXPENSE,
            category=category,
            description="",
        )


def test_invalid_type_raises(category):
    with pytest.raises(ValueError):
        Transaction(
            amount=10.0,
            date="2026-06-01",
            type=TransactionType("invalid"),
            category=category,
            description="x",
        )
