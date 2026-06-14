import pytest

from models.Category import Category


def test_valid_category():
    cat = Category(name="Food", limit=500.0)
    assert cat.name == "Food"
    assert cat.limit == 500.0


def test_zero_limit_is_valid():
    cat = Category(name="Misc", limit=0.0)
    assert cat.limit == 0.0


def test_empty_name_raises():
    with pytest.raises(ValueError, match="name cannot be empty"):
        Category(name="", limit=100.0)


def test_negative_limit_raises():
    with pytest.raises(ValueError, match="limit cannot be negative"):
        Category(name="Food", limit=-1.0)
