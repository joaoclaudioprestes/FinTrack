import pytest

from models.Report import Report
from repositories.SQLiteReportRepository import SQLiteReportRepository


@pytest.fixture
def repo(tmp_path):
    return SQLiteReportRepository(db_path=str(tmp_path / "test.db"))


@pytest.fixture
def report() -> Report:
    return Report(
        month="2026-06",
        total_income=3000.0,
        total_expense=1200.0,
        net_balance=1800.0,
    )


def test_save_and_get_by_month(repo, report):
    repo.save(report)
    found = repo.get_by_month(report.month)
    assert found == report


def test_get_by_month_returns_none_for_missing(repo):
    assert repo.get_by_month("2000-01") is None


def test_save_upserts_existing_month(repo, report):
    repo.save(report)
    updated = Report(
        month=report.month,
        total_income=5000.0,
        total_expense=2000.0,
        net_balance=3000.0,
    )
    repo.save(updated)
    found = repo.get_by_month(report.month)
    assert found.total_income == 5000.0
    assert found.net_balance == 3000.0


def test_list_all_returns_ordered_by_month(repo):
    repo.save(
        Report(
            month="2026-03", total_income=1000.0, total_expense=500.0, net_balance=500.0
        )
    )
    repo.save(
        Report(
            month="2026-01",
            total_income=2000.0,
            total_expense=800.0,
            net_balance=1200.0,
        )
    )
    repo.save(
        Report(
            month="2026-06",
            total_income=3000.0,
            total_expense=1200.0,
            net_balance=1800.0,
        )
    )
    result = repo.list_all()
    assert [r.month for r in result] == ["2026-01", "2026-03", "2026-06"]


def test_list_all_empty_on_new_db(repo):
    assert repo.list_all() == []


def test_delete_removes_report(repo, report):
    repo.save(report)
    repo.delete(report.month)
    assert repo.get_by_month(report.month) is None


def test_delete_nonexistent_does_not_raise(repo):
    repo.delete("1999-12")


def test_persisted_values_match_original(repo, report):
    repo.save(report)
    found = repo.get_by_month(report.month)
    assert found.total_income == report.total_income
    assert found.total_expense == report.total_expense
    assert found.net_balance == report.net_balance
