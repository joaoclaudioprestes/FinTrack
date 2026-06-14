from dataclasses import dataclass

from models.Category import Category
from models.enums import TransactionType


@dataclass(slots=True)
class Transaction:
    amount: float
    date: str
    type: TransactionType
    category: Category
    description: str
    id: int | None = None

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if not self.date:
            raise ValueError("Date cannot be empty.")
        if not self.description:
            raise ValueError("Description cannot be empty.")
