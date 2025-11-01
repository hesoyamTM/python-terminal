from src.application.interfaces.command import Command
import os
import shutil
import uuid


class MvCommand(Command):
    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        # TODO: check length of args
        if len(args) < 2:
            return ""
        if len(args) > 2:
            return ""

        source_path = os.path.expanduser(args[0])
        destination_path = os.path.expanduser(args[1])

        shutil.move(source_path, destination_path)
        return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        source_path = os.path.expanduser(args[0])
        destination_path = os.path.expanduser(args[1])

        shutil.move(destination_path, source_path)

        return ""

    def is_cancelable(self) -> bool:
        return True

    def needs_confirmation(self) -> bool:
        return False
