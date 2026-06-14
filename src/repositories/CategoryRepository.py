from abc import ABC, abstractmethod

from models.Category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def create(self, category: Category) -> Category: ...

    @abstractmethod
    def get_by_name(self, name: str) -> Category | None: ...

    @abstractmethod
    def list_all(self) -> list[Category]: ...

    @abstractmethod
    def update(self, category: Category) -> Category: ...

    @abstractmethod
    def delete(self, name: str) -> None: ...
