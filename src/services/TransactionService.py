from models.Transaction import Transaction
from repositories.TransactionRepository import TransactionRepository
from services.AlertService import AlertService


class TransactionService:
    def __init__(
        self, repository: TransactionRepository, alert_service: AlertService
    ) -> None:
        self._repository = repository
        self._alert_service = alert_service

    def create(self, transaction: Transaction) -> Transaction:
        saved = self._repository.create(transaction)
        alert = self._alert_service.check_limit(saved.category, saved.date[:7])
        if alert:
            print(alert)
        return saved

    def get(self, transaction_id: int) -> Transaction | None:
        return self._repository.get_by_id(transaction_id)

    def list_all(self) -> list[Transaction]:
        return self._repository.list_all()

    def update(self, transaction: Transaction) -> Transaction:
        return self._repository.update(transaction)

    def delete(self, transaction_id: int) -> None:
        self._repository.delete(transaction_id)
