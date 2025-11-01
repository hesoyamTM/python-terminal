from src.application.interfaces.command import Command
from src.application.errors.commands import ArgumentError
import os
import uuid


class CdCommand(Command):
    """
    cd <directory>
    """

    def __init__(self, environment):
        """
        :param environment: FileSystemEnvironment
        """
        self.environment = environment

    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        """
        Executes the command
        :param id: uuid.UUID
        :param args: list[str]
        :param flags: list[str]
        :return: str
        """

        if len(args) != 1:
            raise ArgumentError("cd requires exactly one argument")

        path = os.path.expanduser(args[0])

        os.chdir(path)

        return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        """
        Undoes the command
        :param id: uuid.UUID
        :param args: list[str]
        :param flags: list[str]
        :return: str
        """
        return ""

    def is_cancelable(self) -> bool:
        """
        :return: bool
        """
        return False

    def needs_confirmation(self) -> bool:
        """
        :return: bool
        """
        return False
