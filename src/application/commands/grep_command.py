from src.application.interfaces.command import Command
from src.application.errors.file import FileIsADirectoryError
from typing import Iterator
from src.application.interfaces.environment import FileSystemEnvironment
from src.application.errors.commands import ArgumentError
import re
import uuid
import os


class GrepCommand(Command):
    """
    grep [-ir] <pattern> <file>
    """

    def __init__(self, env: FileSystemEnvironment):
        """
        :param env: FileSystemEnvironment
        """
        self.env = env
        pass

    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        """
        Executes the command
        :param id: uuid.UUID
        :param args: list[str]
        :param flags: list[str]
        :return: str
        """

        if len(args) != 2:
            raise ArgumentError("grep requires exactly two arguments")

        pattern = args[0]
        source_path = self.env.normalize_path(args[1])

        flag = "".join(flags)
        ignore_case = "i" in flag
        res: str = ""

        if self.env.is_directory(source_path):
            if "r" in flag:
                res = "\n".join(self.grep_directory(pattern, source_path, ignore_case))
            else:
                raise FileIsADirectoryError(source_path)
        else:
            res = "\n".join(self.grep_file(pattern, source_path, ignore_case))

        return res

    def grep_file(
        self, pattern: str, file_path: str, ignore_case=False
    ) -> Iterator[str]:
        """
        Find pattern in file
        :param pattern: str
        :param file_path: str
        :param ignore_case: bool
        :return: Iterator[str]
        """

        compiled_pattern = re.compile(pattern, re.IGNORECASE if ignore_case else 0)

        try:
            for i, line in enumerate(self.env.read_lines(file_path)):
                for match in compiled_pattern.finditer(line):
                    yield f"{file_path}: {i + 1}:{match.start()}: {self.colorize_match(line, match)}"
        except UnicodeDecodeError:
            return

    def grep_directory(
        self, pattern: str, directory_path: str, ignore_case=False
    ) -> Iterator[str]:
        queue = [directory_path]

        while queue:
            current_path = queue.pop(0)
            for file in self.env.get_directory_list(current_path):
                file_path = os.path.join(current_path, file)
                if self.env.is_file(file_path):
                    yield from self.grep_file(pattern, file_path, ignore_case)
                elif self.env.is_directory(file_path):
                    queue.append(file_path)

    def colorize_match(self, line: str, match: re.Match[str]) -> str:
        return f"{line[: match.start()]}\033[1;31m{line[match.start() : match.end()]}\033[0m{line[match.end() :]}".replace(
            "\n", ""
        )

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return False

    def needs_confirmation(self) -> bool:
        return False
