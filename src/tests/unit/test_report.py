import pytest

from models.Report import Report


def test_valid_report():
    r = Report(
        month="2026-06", total_income=3000.0, total_expense=1200.0, net_balance=1800.0
    )
    assert r.month == "2026-06"
    assert r.net_balance == 1800.0


def test_month_without_transactions_is_valid():
    r = Report(month="2026-06", total_income=0.0, total_expense=0.0, net_balance=0.0)
    assert r.total_income == 0.0
    assert r.total_expense == 0.0
    assert r.net_balance == 0.0


def test_negative_net_balance_is_valid():
    r = Report(
        month="2026-06", total_income=500.0, total_expense=1200.0, net_balance=-700.0
    )
    assert r.net_balance == -700.0


def test_empty_month_raises():
    with pytest.raises(ValueError, match="Month cannot be empty"):
        Report(month="", total_income=0.0, total_expense=0.0, net_balance=0.0)


def test_negative_total_income_raises():
    with pytest.raises(ValueError, match="income cannot be negative"):
        Report(month="2026-06", total_income=-1.0, total_expense=0.0, net_balance=0.0)


def test_negative_total_expense_raises():
    with pytest.raises(ValueError, match="expense cannot be negative"):
        Report(month="2026-06", total_income=0.0, total_expense=-1.0, net_balance=0.0)
