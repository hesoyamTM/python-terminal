from typing import Tuple
import re


class Parser:
    """
    Parses command
    """

    _re_command: re.Pattern

    def __init__(self):
        self._re_command = re.compile(
            r"^(?P<command>\w+)(?P<flags>(\ -.+?))?(?P<args>(\ .+))?$"
        )

    def parse(self, command: str) -> Tuple[str, list[str], list[str]]:
        """
        Parses command
        :param command: command to parse
        :return: tuple of command name, args and flags
        """
        match = self._re_command.match(command)

        if match is None:
            raise ValueError(f"Invalid command: {command}")

        command_name: str = match.group("command") or ""
        args_str: str = match.group("args") or ""
        flags_str: str = match.group("flags") or ""

        # [1:] removes the first space
        args: list[str] = args_str[1:].split(" ") if args_str else []
        flags: list[str] = flags_str[1:].split(" ") if flags_str else []

        return command_name, args, flags
