from src.application.interfaces.command import Command
from src.application.interfaces.history import HistoryRepository
from src.application.errors.commands import ArgumentError
import uuid


class HistoryCommand(Command):
    _history_repository: HistoryRepository

    def __init__(self, history_repository: HistoryRepository):
        self._history_repository = history_repository

    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        if len(args) != 0:
            raise ArgumentError("History command does not take arguments")

        return "".join(self._history_repository.get())

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return False

    def needs_confirmation(self) -> bool:
        return False
