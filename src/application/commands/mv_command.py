from src.application.interfaces.command import Command
import os
import shutil


class MvCommand(Command):
    def do(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        # TODO: check length of args
        if len(args) < 2:
            return ""
        if len(args) > 2:
            return ""

        source_path = os.path.expanduser(args[0])
        destination_path = os.path.expanduser(args[1])

        shutil.move(source_path, destination_path)
        return ""

    def undo(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return True

    def needs_confirmation(self) -> bool:
        return False
