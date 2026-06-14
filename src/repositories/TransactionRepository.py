from abc import ABC, abstractmethod

from models.Transaction import Transaction


class TransactionRepository(ABC):
    @abstractmethod
    def create(self, transaction: Transaction) -> Transaction: ...

    @abstractmethod
    def get_by_id(self, transaction_id: int) -> Transaction | None: ...

    @abstractmethod
    def list_all(self) -> list[Transaction]: ...

    @abstractmethod
    def update(self, transaction: Transaction) -> Transaction: ...

    @abstractmethod
    def delete(self, transaction_id: int) -> None: ...
