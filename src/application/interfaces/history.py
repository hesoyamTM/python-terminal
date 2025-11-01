from abc import ABC, abstractmethod
from typing import Tuple
import uuid


class HistoryRepository(ABC):
    """
    History repository
    """

    @abstractmethod
    def add(self, id: uuid.UUID, command: str) -> None:
        """
        Add command to history
        """
        pass

    @abstractmethod
    def get(self) -> list[str]:
        """
        Get history
        """
        pass

    @abstractmethod
    def pop(self) -> Tuple[uuid.UUID, str]:
        """
        Pop command from history
        """
        pass
