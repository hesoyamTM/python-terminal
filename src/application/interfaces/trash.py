from abc import ABC, abstractmethod
from typing import Iterator
import uuid


class TrashRepository(ABC):
    @abstractmethod
    def add(self, id: uuid.UUID, file_tree: dict[str, dict | str]) -> None:
        pass

    @abstractmethod
    def get(self) -> Iterator[dict[str, dict | str]]:
        pass

    @abstractmethod
    def get_by_id(self, id: uuid.UUID) -> dict[str, dict | str] | None:
        pass
