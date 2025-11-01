from src.application.interfaces.command import Command
import os
import shutil
import uuid


class TarCommand(Command):
    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        # TODO: check length of args
        if len(args) < 2:
            return ""
        if len(args) > 2:
            return ""

        source_path = os.path.normpath(os.path.expanduser(args[0]))
        destination_path = os.path.normpath(os.path.expanduser(args[1]))

        if os.path.isdir(source_path):
            shutil.make_archive(destination_path, "tar", source_path)
        else:
            # TODO: Error
            pass

        return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return False

    def needs_confirmation(self) -> bool:
        return False
