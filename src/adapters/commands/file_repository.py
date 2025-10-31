from src.application.interfaces.history import HistoryRepository
from src.constants import HISTORY_FILE


class FileHistoryRepository(HistoryRepository):
    """
    File history repository
    """

    def add(self, command: str) -> None:
        """
        Add command to history
        """
        with open(HISTORY_FILE, "a") as f:
            f.write(command)
            f.write("\n")

    def get(self) -> list[str]:
        """
        Get history
        """

        with open(HISTORY_FILE, "r") as f:
            return f.readlines()

    def pop(self) -> str:
        """
        Pop command from history
        """

        with open(HISTORY_FILE, "r") as f:
            return f.readlines()[-1]
