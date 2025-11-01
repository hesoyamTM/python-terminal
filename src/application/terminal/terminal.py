from src.application.commands.undo_command import UndoCommand
from src.application.interfaces.environment import FileSystemEnvironment
from src.application.interfaces.terminal import TerminalInterface
from src.application.interfaces.history import HistoryRepository
from src.application.interfaces.trash import TrashRepository
from src.application.terminal.parser import Parser
from src.application.interfaces.command import Command
import uuid

from src.application.commands.cd_command import CdCommand
from src.application.commands.cat_command import CatCommand
from src.application.commands.cp_command import CpCommand
from src.application.commands.grep_command import GrepCommand
from src.application.commands.ls_command import LsCommand
from src.application.commands.mv_command import MvCommand
from src.application.commands.rm_command import RmCommand
from src.application.commands.tar_command import TarCommand
from src.application.commands.untar_command import UntarCommand
from src.application.commands.unzip_command import UnzipCommand
from src.application.commands.zip_command import ZipCommand
from src.application.commands.history_command import HistoryCommand

import src.application.errors.commands as commands_errors


class TerminalService(TerminalInterface):
    """
    Executes commands
    """

    _history_repository: HistoryRepository
    _cancelable_history_repository: HistoryRepository
    _commands: dict[str, Command]
    _environment: FileSystemEnvironment

    _parser: Parser

    def __init__(
        self,
        history_repository: HistoryRepository,
        cancelable_history_repository: HistoryRepository,
        trash_repository: TrashRepository,
        environment: FileSystemEnvironment,
        parser: Parser,
    ):
        self._cancelable_history_repository = cancelable_history_repository
        self._history_repository = history_repository
        self._parser = parser
        self._environment = environment

        self._commands = {
            "cd": CdCommand(environment),
            "cat": CatCommand(environment),
            "cp": CpCommand(environment),
            "grep": GrepCommand(environment),
            "ls": LsCommand(environment),
            "mv": MvCommand(environment),
            "rm": RmCommand(trash_repository, environment),
            "tar": TarCommand(environment),
            "untar": UntarCommand(environment),
            "unzip": UnzipCommand(environment),
            "zip": ZipCommand(environment),
            "history": HistoryCommand(history_repository),
        }
        self._commands["undo"] = UndoCommand(
            self._commands, cancelable_history_repository, parser
        )

    def execute(self, command: str) -> str:
        """
        Executes command
        """

        command_name, args, flags = self._parser.parse(command)

        if command_name in self._commands:
            cmd = self._commands[command_name]
            id = uuid.uuid4()

            if cmd.is_cancelable():
                self._cancelable_history_repository.add(id, command)

            self._history_repository.add(id, command)

            return cmd.do(id, args, flags)

        raise commands_errors.CommandNotFoundError(command_name)

    def needs_confirmation(self, command) -> bool:
        """
        Returns True if needs confirmation
        """

        command_name, _, _ = self._parser.parse(command)

        if command_name in self._commands:
            return self._commands[command_name].needs_confirmation()

        return False

    def get_current_directory(self) -> str:
        """
        Returns current directory
        """
        return self._environment.get_current_directory()
