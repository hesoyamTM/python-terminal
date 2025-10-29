from src.domain.commands.repository import HistoryRepository


class InMemoryHistoryRepository(HistoryRepository):
    """
    In-memory history repository
    """

    _history: list[str]

    def __init__(self):
        """
        Initializes the history repository
        """
        self._history: list[str] = []

    def add(self, command: str) -> None:
        """
        Add command to history
        """
        self._history.append(command)

    def get(self) -> list[str]:
        """
        Get history
        """
        return self._history

    def pop(self) -> str:
        """
        Pop command from history
        """
        return self._history.pop()
