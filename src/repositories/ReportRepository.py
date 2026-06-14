from abc import ABC, abstractmethod

from models.Report import Report


class ReportRepository(ABC):
    @abstractmethod
    def save(self, report: Report) -> Report: ...

    @abstractmethod
    def get_by_month(self, month: str) -> Report | None: ...

    @abstractmethod
    def list_all(self) -> list[Report]: ...

    @abstractmethod
    def delete(self, month: str) -> None: ...
