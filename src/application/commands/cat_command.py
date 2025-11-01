from src.application.interfaces.command import Command
from src.application.errors.commands import ArgumentError
import uuid
import src.application.errors.file as errors


class CatCommand(Command):
    """
    cat <file>
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
            raise ArgumentError("cat requires exactly one argument")

        file: str = args[0]

        try:
            content: str = self.environment.read_file(file)
        except FileNotFoundError:
            raise errors.FileNotFoundError(file)

        return content

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
