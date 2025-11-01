from src.application.interfaces.command import Command
from typing import Iterator
import os
import re
import uuid


class GrepCommand(Command):
    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        # TODO: check length of args
        if len(args) < 2:
            return ""
        if len(args) > 2:
            return ""

        pattern = args[0]
        source_path = os.path.normpath(os.path.expanduser(args[1]))

        flag = "".join(flags)
        ignore_case = "i" in flag
        res: str = ""

        if "r" in flag:
            res = "\n".join(self.grep_directory(pattern, source_path, ignore_case))
        else:
            res = "\n".join(self.grep_file(pattern, source_path, ignore_case))

        return res

    def grep_file(
        self, pattern: str, file_path: str, ignore_case=False
    ) -> Iterator[str]:
        compiled_pattern = re.compile(pattern)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for i, line in enumerate(file):
                    for match in compiled_pattern.finditer(
                        line, re.IGNORECASE if ignore_case else 0
                    ):
                        yield f"{file_path}: {i}:{match.start()}: {self.colorize_match(line, match)}"
        except UnicodeDecodeError:
            return

    def grep_directory(
        self, pattern: str, directory_path: str, ignore_case=False
    ) -> Iterator[str]:
        queue = [directory_path]

        while queue:
            current_path = queue.pop(0)
            for file in os.listdir(current_path):
                file_path = os.path.join(current_path, file)
                if os.path.isfile(file_path):
                    yield from self.grep_file(pattern, file_path, ignore_case)
                elif os.path.isdir(file_path):
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
