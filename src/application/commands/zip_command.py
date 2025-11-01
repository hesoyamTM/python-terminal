from src.application.interfaces.command import Command
from src.application.interfaces.environment import FileSystemEnvironment
from src.application.errors.commands import ArgumentError
import uuid


class ZipCommand(Command):
    """
    zip <source> <destination>
    """

    def __init__(self, env: FileSystemEnvironment):
        """
        :param env: FileSystemEnvironment
        """
        self.env = env

    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        if len(args) != 2:
            raise ArgumentError("zip requires exactly two arguments")

        source_path = self.env.normalize_path(args[0])
        destination_path = self.env.normalize_path(args[1])

        if self.env.is_directory(source_path):
            self.env.make_archive(source_path, destination_path, "zip")
        else:
            self.env.create_directory(destination_path)
            self.env.copy_file(source_path, destination_path)
            self.env.make_archive(destination_path, destination_path, "zip")
            self.env.delete_directory(destination_path)

        return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return False

    def needs_confirmation(self) -> bool:
        return False
