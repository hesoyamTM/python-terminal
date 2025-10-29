from src.domain.commands.command_interface import Command


class CatCommand(Command):
    def do(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        if len(args) == 0:
            return ""

        file: str = args[0]
        with open(file, "r") as f:
            return f.read()

    def undo(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return False

    def needs_confirmation(self) -> bool:
        return False
