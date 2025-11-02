from typing import Iterator
from src.application.interfaces.command import Command
from src.application.interfaces.environment import FileSystemEnvironment

# from src.application.errors.commands import ArgumentError
import uuid


class LsCommand(Command):
    """
    ls [-a] [-l] [path...]
    """

    def __init__(self, env: FileSystemEnvironment):
        """
        :param env: FileSystemEnvironment
        """
        self.env = env

    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        """
        Executes the command
        :param id: uuid.UUID
        :param args: list[str]
        :param flags: list[str]
        :return: str
        """
        res: str = ""

        if len(args) == 0:
            args = [self.env.get_current_directory()]

        if len(args) == 1:
            for file in self.get_files(args[0], flags):
                res += f"{file}\n"
            return res

        for i, path in enumerate(args):
            if i > 0:
                res += "\n"

            res += f"{path}:\n"
            for file in self.get_files(path, flags):
                res += f"{file}\n"

        return res[:-1]

    def get_files(self, arg: str, flags: list[str]) -> Iterator[str]:
        path = self.env.normalize_path(arg)

        flag: str = "".join(flags)

        for file in sorted(self.env.get_directory_list(path) + ["."] + [".."]):
            if file.startswith(".") and "a" not in flag:
                continue

            try:
                if "l" in flag:
                    yield self.env.get_file_info(path, file)
                else:
                    yield file
            except StopIteration:
                return

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return False

    def needs_confirmation(self) -> bool:
        return False
