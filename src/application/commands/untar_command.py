from src.application.interfaces.command import Command
import os
import shutil
import uuid


class UntarCommand(Command):
    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        # TODO: check length of args
        if len(args) < 1:
            return ""
        if len(args) > 1:
            return ""

        source_path = os.path.normpath(os.path.expanduser(args[0]))

        shutil.unpack_archive(source_path, format="tar")

        return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return False

    def needs_confirmation(self) -> bool:
        return False
