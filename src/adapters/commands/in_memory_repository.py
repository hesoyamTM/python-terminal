from src.application.interfaces.history import HistoryRepository
import uuid
from typing import Tuple


class InMemoryHistoryRepository(HistoryRepository):
    """
    In-memory history repository
    """

    _history: list[Tuple[uuid.UUID, str]]

    def __init__(self):
        """
        Initializes the history repository
        """
        self._history: list[Tuple[uuid.UUID, str]] = []

    def add(self, id: uuid.UUID, command: str) -> None:
        """
        Add command to history
        """
        self._history.append((id, command))

    def get(self) -> list[str]:
        """
        Get history
        """
        return [command for _, command in self._history]

    def pop(self) -> Tuple[uuid.UUID, str]:
        """
        op command from history
        """
        id, command = self._history.pop()
        return (id, command)
