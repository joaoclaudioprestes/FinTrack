from models.Category import Category
from models.enums import TransactionType
from repositories.TransactionRepository import TransactionRepository


class AlertService:
    def __init__(self, transaction_repository: TransactionRepository) -> None:
        self._repository = transaction_repository

    def check_limit(self, category: Category, month: str) -> str | None:
        """Returns an alert message if the category expense exceeded its limit for the given month (YYYY-MM), otherwise None."""
        if category.limit == 0.0:
            return None

        total_spent = sum(
            t.amount
            for t in self._repository.list_all()
            if t.category.name == category.name
            and t.date.startswith(month)
            and t.type == TransactionType.EXPENSE
        )

        if total_spent > category.limit:
            return (
                f"Atenção: gasto de R${total_spent:,.2f} excedeu o limite de "
                f"R${category.limit:,.2f} para '{category.name}' em {month}."
            )
        return None

    def list_exceeded(self, month: str) -> list[str]:
        """Returns alert messages for all categories that exceeded their limit in the given month."""
        transactions = [
            t for t in self._repository.list_all() if t.date.startswith(month)
        ]

        spent_by_category: dict[str, tuple[float, float]] = {}
        for t in transactions:
            if t.type == TransactionType.EXPENSE:
                name = t.category.name
                limit = t.category.limit
                total, _ = spent_by_category.get(name, (0.0, limit))
                spent_by_category[name] = (total + t.amount, limit)

        return [
            f"'{name}': R${spent:,.2f} / limite R${limit:,.2f}"
            for name, (spent, limit) in spent_by_category.items()
            if limit > 0.0 and spent > limit
        ]
