from src.application.interfaces.command import Command
import src.application.errors.commands as errors
import os
import shutil
import uuid


class CpCommand(Command):
    """
    cp [-r] <source> <destination>
    """

    def __init__(self, environment):
        """
        :param environment: FileSystemEnvironment
        """
        self.environment = environment

    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        if len(args) != 2:
            raise errors.ArgumentError("cp requires exactly two arguments")

        source_path = os.path.expanduser(args[0])
        destination_path = os.path.expanduser(args[1])

        flag = "".join(flags)

        if self.environment.is_directory(source_path):
            if "r" in flag:
                self.environment.copy_directory(source_path, destination_path)
                return ""
            else:
                # TODO: error
                return ""

        shutil.copy(source_path, destination_path)
        return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        destination_path = os.path.expanduser(args[1])

        if os.path.isdir(destination_path):
            shutil.rmtree(destination_path)
        else:
            os.remove(destination_path)

        return ""

    def is_cancelable(self) -> bool:
        return True

    def needs_confirmation(self) -> bool:
        return False
