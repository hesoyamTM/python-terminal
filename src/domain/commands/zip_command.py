from src.domain.commands.command_interface import Command
import os
import shutil


class ZipCommand(Command):
    def do(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        # TODO: check length of args
        if len(args) < 2:
            return ""
        if len(args) > 2:
            return ""

        source_path = os.path.normpath(os.path.expanduser(args[0]))
        destination_path = os.path.normpath(os.path.expanduser(args[1]))

        if os.path.isdir(source_path):
            shutil.make_archive(destination_path, "zip", source_path)
        else:
            # TODO: Error
            pass

        return ""

    def undo(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return True

    def needs_confirmation(self) -> bool:
        return False
