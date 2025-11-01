from src.application.interfaces.history import HistoryRepository
from typing import Tuple
import uuid


class FileHistoryRepository(HistoryRepository):
    """
    File history repository
    """

    _file_path: str

    def __init__(self, file_path: str) -> None:
        """
        Initialize history repository
        """
        self._file_path = file_path

    def add(self, id: uuid.UUID, command: str) -> None:
        """
        Add command to history
        """
        with open(self._file_path, "a") as f:
            f.write(f"{id} {command}\n")

    def get(self) -> list[str]:
        """
        Get history
        """

        with open(self._file_path, "r") as f:
            return [line.split(" ", 1)[1] for line in f.readlines() if line != ""]

    def pop(self) -> Tuple[uuid.UUID, str]:
        """
        Pop command from history
        """

        with open(self._file_path, "r+") as f:
            f.seek(0, 2)
            file_size = f.tell()

            if file_size > 0:
                file_size -= 1

            pos = file_size - 1
            while pos > 0:
                f.seek(pos)
                if f.read(1) == "\n":
                    break
                pos -= 1

            if pos == 0:
                f.seek(0)

            line = f.read().split(" ", 1)
            id = line[0]
            command = line[1].strip()

            f.truncate(pos)

            return (uuid.UUID(id), command)
