import pytest

from models.Category import Category
from repositories.SQLiteCategoryRepository import SQLiteCategoryRepository


@pytest.fixture
def repo(tmp_path):
    return SQLiteCategoryRepository(db_path=str(tmp_path / "test.db"))


def test_create_and_get_by_name(repo, category):
    repo.create(category)
    found = repo.get_by_name(category.name)
    assert found == category


def test_get_by_name_returns_none_for_missing(repo):
    assert repo.get_by_name("Unknown") is None


def test_list_all_returns_all(repo):
    repo.create(Category(name="Food", limit=500.0))
    repo.create(Category(name="Transport", limit=200.0))
    result = repo.list_all()
    assert len(result) == 2
    names = {c.name for c in result}
    assert names == {"Food", "Transport"}


def test_list_all_empty_on_new_db(repo):
    assert repo.list_all() == []


def test_update_persists_new_limit(repo, category):
    repo.create(category)
    updated = Category(name=category.name, limit=999.0)
    repo.update(updated)
    found = repo.get_by_name(category.name)
    assert found.limit == 999.0


def test_delete_removes_category(repo, category):
    repo.create(category)
    repo.delete(category.name)
    assert repo.get_by_name(category.name) is None


def test_delete_nonexistent_does_not_raise(repo):
    repo.delete("Ghost")


def test_create_returns_original_category(repo, category):
    result = repo.create(category)
    assert result == category
