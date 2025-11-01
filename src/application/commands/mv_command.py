from src.application.interfaces.command import Command
from src.application.interfaces.environment import FileSystemEnvironment
from src.application.errors.commands import ArgumentError
import uuid


class MvCommand(Command):
    """
    mv <source> <destination>
    """

    def __init__(self, env: FileSystemEnvironment):
        """
        :param environment: FileSystemEnvironment
        """
        self.env = env

    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        if len(args) != 2:
            raise ArgumentError("mv requires exactly two arguments")

        source_path = self.env.normalize_path(args[0])
        destination_path = self.env.normalize_path(args[1])

        self.env.move(source_path, destination_path)
        return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        source_path = self.env.normalize_path(args[0])
        destination_path = self.env.normalize_path(args[1])

        self.env.move(destination_path, source_path)

        return ""

    def is_cancelable(self) -> bool:
        return True

    def needs_confirmation(self) -> bool:
        return False
