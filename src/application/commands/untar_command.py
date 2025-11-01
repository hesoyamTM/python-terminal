from src.application.interfaces.command import Command
from src.application.interfaces.environment import FileSystemEnvironment
from src.application.errors.commands import ArgumentError
import uuid


class UntarCommand(Command):
    """
    untar <file>
    """

    def __init__(self, env: FileSystemEnvironment):
        """
        :param env: FileSystemEnvironment
        """
        self.env = env

    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        if len(args) != 1:
            raise ArgumentError("untar requires exactly one argument")

        source_path = self.env.normalize_path(args[0])

        self.env.extract_archive(source_path, self.env.get_current_directory(), "tar")

        return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return False

    def needs_confirmation(self) -> bool:
        return False
