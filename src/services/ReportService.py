from models.enums import TransactionType
from models.Report import Report
from repositories.TransactionRepository import TransactionRepository


class ReportService:
    def __init__(self, transaction_repository: TransactionRepository) -> None:
        self._repository = transaction_repository

    def generate_monthly(self, month: str) -> Report:
        """Generate a monthly report. month format: YYYY-MM"""
        transactions = [
            t for t in self._repository.list_all() if t.date.startswith(month)
        ]
        total_income = sum(
            t.amount for t in transactions if t.type == TransactionType.INCOME
        )
        total_expense = sum(
            t.amount for t in transactions if t.type == TransactionType.EXPENSE
        )
        return Report(
            month=month,
            total_income=total_income,
            total_expense=total_expense,
            net_balance=total_income - total_expense,
        )
