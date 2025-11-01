from src.application.interfaces.command import Command
import src.application.errors.commands as errors
import src.application.errors.file as files_errors
from src.application.interfaces.environment import FileSystemEnvironment
import uuid


class CpCommand(Command):
    """
    cp [-r] <source> <destination>
    """

    def __init__(self, environment: FileSystemEnvironment):
        """
        :param environment: FileSystemEnvironment
        """
        self.environment = environment

    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        if len(args) != 2:
            raise errors.ArgumentError("cp requires exactly two arguments")

        source_path = self.environment.normalize_path(args[0])
        destination_path = self.environment.normalize_path(args[1])

        flag = "".join(flags)

        if self.environment.is_directory(source_path):
            if "r" in flag:
                self.environment.copy_directory(source_path, destination_path)
                return ""
            else:
                raise files_errors.DirectoryIsAFileError(source_path)
        else:
            self.environment.copy_file(source_path, destination_path)
            return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        destination_path = self.environment.normalize_path(args[1])

        if self.environment.is_directory(destination_path):
            self.environment.delete_directory(destination_path)
        else:
            self.environment.delete_file(destination_path)

        return ""

    def is_cancelable(self) -> bool:
        return True

    def needs_confirmation(self) -> bool:
        return False
