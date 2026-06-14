from dataclasses import dataclass


@dataclass(slots=True)
class Report:
    month: str
    total_income: float
    total_expense: float
    net_balance: float

    def __post_init__(self):
        if not self.month:
            raise ValueError("Month cannot be empty.")
        if self.total_income < 0:
            raise ValueError("Total income cannot be negative.")
        if self.total_expense < 0:
            raise ValueError("Total expense cannot be negative.")
