import pytest

from models.enums import TransactionType
from models.Transaction import Transaction
from repositories.SQLiteTransactionRepository import SQLiteTransactionRepository


@pytest.fixture
def repo(tmp_path):
    return SQLiteTransactionRepository(db_path=str(tmp_path / "test.db"))


def test_create_assigns_id(repo, transaction):
    saved = repo.create(transaction)
    assert saved.id == 1


def test_create_multiple_ids_are_unique(repo, transaction):
    first = repo.create(transaction)
    second = repo.create(transaction)
    assert first.id != second.id


def test_get_by_id_returns_saved_transaction(repo, transaction):
    saved = repo.create(transaction)
    found = repo.get_by_id(saved.id)
    assert found == saved


def test_get_by_id_returns_none_for_missing(repo):
    assert repo.get_by_id(999) is None


def test_list_all_returns_all(repo, transaction):
    repo.create(transaction)
    repo.create(transaction)
    assert len(repo.list_all()) == 2


def test_list_all_empty_on_new_db(repo):
    assert repo.list_all() == []


def test_update_persists_changes(repo, transaction):
    saved = repo.create(transaction)
    updated = Transaction(
        id=saved.id,
        amount=250.0,
        date="2026-06-15",
        type=TransactionType.INCOME,
        category=saved.category,
        description="Salary",
    )
    repo.update(updated)
    found = repo.get_by_id(saved.id)
    assert found.amount == 250.0
    assert found.type == TransactionType.INCOME
    assert found.description == "Salary"


def test_delete_removes_transaction(repo, transaction):
    saved = repo.create(transaction)
    repo.delete(saved.id)
    assert repo.get_by_id(saved.id) is None


def test_delete_nonexistent_does_not_raise(repo):
    repo.delete(999)


def test_persisted_values_match_original(repo, transaction):
    saved = repo.create(transaction)
    found = repo.get_by_id(saved.id)
    assert found.amount == transaction.amount
    assert found.date == transaction.date
    assert found.type == transaction.type
    assert found.category.name == transaction.category.name
    assert found.category.limit == transaction.category.limit
    assert found.description == transaction.description
