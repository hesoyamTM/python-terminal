from src.application.interfaces.command import Command
import os
import uuid


class CdCommand(Command):
    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        if len(args) == 0:
            return ""

        if len(args) == 1:
            path = os.path.expanduser(args[0])

            # TODO: check if path is a directory
            # if not os.path.exists(path):
            #     return ""

            os.chdir(path)
            return ""

        return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return False

    def needs_confirmation(self) -> bool:
        return False
