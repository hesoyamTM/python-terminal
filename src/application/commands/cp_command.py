from src.application.interfaces.command import Command
import os
import shutil
import uuid


class CpCommand(Command):
    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        # TODO: check length of args
        if len(args) < 2:
            return ""
        if len(args) > 2:
            return ""

        source_path = os.path.expanduser(args[0])
        destination_path = os.path.expanduser(args[1])

        flag = "".join(flags)

        if os.path.isdir(source_path):
            if "r" in flag:
                shutil.copytree(source_path, destination_path)
                return ""
            else:
                # TODO: error
                return ""

        shutil.copy(source_path, destination_path)
        return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        destination_path = os.path.expanduser(args[1])

        if os.path.isdir(destination_path):
            shutil.rmtree(destination_path)
        else:
            os.remove(destination_path)

        return ""

    def is_cancelable(self) -> bool:
        return True

    def needs_confirmation(self) -> bool:
        return False
