from dataclasses import dataclass


@dataclass(slots=True)
class Category:
    name: str
    limit: float

    def __post_init__(self):
        if not self.name:
            raise ValueError("Category name cannot be empty.")
        if self.limit < 0:
            raise ValueError("Category limit cannot be negative.")
