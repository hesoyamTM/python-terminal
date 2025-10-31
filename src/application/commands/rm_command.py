from src.application.interfaces.command import Command
import os
import shutil


class RmCommand(Command):
    def do(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        # TODO: check length of args
        if len(args) < 1:
            return ""
        if len(args) > 1:
            return ""

        source_path = os.path.normpath(os.path.expanduser(args[0]))

        flag = "".join(flags)

        if os.path.isdir(source_path):
            if "r" in flag:
                if source_path in os.path.normpath(current_directory):
                    # TODO: return error message
                    return ""
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
