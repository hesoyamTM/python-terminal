from src.application.interfaces.command import Command
import uuid


class CatCommand(Command):
    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        if len(args) == 0:
            return ""

        file: str = args[0]
        with open(file, "r") as f:
            return f.read()

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return False

    def needs_confirmation(self) -> bool:
        return False
