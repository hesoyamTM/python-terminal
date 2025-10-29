from src.domain.commands.command_interface import Command
import os
import shutil


class RmCommand(Command):
    def do(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        # TODO: check length of args
        if len(args) < 1:
            return ""
        if len(args) > 1:
            return ""

        source_path = os.path.expanduser(args[0])

        flag = "".join(flags)

        if os.path.isdir(source_path):
            if "r" in flag:
                shutil.rmtree(source_path)
            else:
                return ""
        elif os.path.isfile(source_path):
            if "f" in flag:
                os.remove(source_path)
            else:
                return ""

        return ""

    def undo(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return True

    def needs_confirmation(self) -> bool:
        return True
