from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def do(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        pass

    @abstractmethod
    def undo(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        pass

    @abstractmethod
    def is_cancelable(self) -> bool:
        pass

    @abstractmethod
    def needs_confirmation(self) -> bool:
        pass
