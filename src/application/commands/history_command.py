from src.application.interfaces.command import Command
from src.application.interfaces.history import HistoryRepository


class HistoryCommand(Command):
    _history_repository: HistoryRepository

    def __init__(self, history_repository: HistoryRepository):
        self._history_repository = history_repository

    def do(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        return "".join(self._history_repository.get())

    def undo(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return False

    def needs_confirmation(self) -> bool:
        return False
