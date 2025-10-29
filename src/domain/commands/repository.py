from abc import ABC, abstractmethod


class HistoryRepository(ABC):
    """
    History repository interface
    """

    @abstractmethod
    def add(self, command: str) -> None:
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
    def pop(self) -> str:
        """
        Pop command from history
        """
        pass
