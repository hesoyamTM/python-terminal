from src.application.interfaces.command import Command
from src.application.interfaces.history import HistoryRepository

# from src.application.interfaces.environment import FileSystemEnvironment
from src.application.errors.commands import ArgumentError
import uuid

from src.application.terminal.parser import Parser


class UndoCommand(Command):
    """
    undo
    """

    _commands: dict[str, Command] = {}
    _history_repository: HistoryRepository
    _parser: Parser

    def __init__(
        self,
        commands: dict[str, Command],
        history_repository: HistoryRepository,
        parser: Parser,
    ):
        self._commands = commands
        self._history_repository = history_repository
        self._parser = parser

    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        if len(args) != 0:
            raise ArgumentError("undo requires no arguments")

        cmd_id, cmd = self._history_repository.pop()

        command_name, args, flags = self._parser.parse(cmd)

        self._commands[command_name].undo(cmd_id, args, flags)

        return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return False

    def needs_confirmation(self) -> bool:
        return False
