from src.application.interfaces.termianal import TerminalInterface
from src.domain.commands.repository import HistoryRepository
from src.application.terminal.parser import Parser
from src.constants import COMMANDS
from os import getcwd


class TerminalService(TerminalInterface):
    """
    Executes commands
    """

    _history_repository: HistoryRepository
    _cancelable_history_repository: HistoryRepository

    _parser: Parser

    def __init__(
        self,
        history_repository: HistoryRepository,
        cancelable_history_repository: HistoryRepository,
        parser: Parser,
    ):
        self._cancelable_history_repository = cancelable_history_repository
        self._history_repository = history_repository
        self._parser = parser

    def execute(self, command: str) -> str:
        """
        Executes command
        """

        command_name, args, flags = self._parser.parse(command)

        if command_name in COMMANDS:
            if COMMANDS[command_name].is_cancelable():
                self._cancelable_history_repository.add(command)

            return COMMANDS[command_name].do(getcwd(), args, flags)

        return f"Command {command_name} not found"

    def needs_confirmation(self, command) -> bool:
        """
        Returns True if needs confirmation
        """

        command_name, _, _ = self._parser.parse(command)

        if command_name in COMMANDS:
            return COMMANDS[command_name].needs_confirmation()

        return False

    def get_current_directory(self) -> str:
        """
        Returns current directory
        """
        return getcwd()
