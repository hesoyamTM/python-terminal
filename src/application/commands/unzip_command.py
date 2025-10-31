from src.application.interfaces.command import Command
import os
import shutil


class UnzipCommand(Command):
    def do(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        # TODO: check length of args
        if len(args) < 1:
            return ""
        if len(args) > 1:
            return ""

        source_path = os.path.normpath(os.path.expanduser(args[0]))

        shutil.unpack_archive(source_path, format="zip")

        return ""

    def undo(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return True

    def needs_confirmation(self) -> bool:
        return False
