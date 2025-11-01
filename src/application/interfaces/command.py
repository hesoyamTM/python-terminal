from abc import ABC, abstractmethod
import uuid


class Command(ABC):
    @abstractmethod
    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        pass

    @abstractmethod
    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        pass

    @abstractmethod
    def is_cancelable(self) -> bool:
        pass

    @abstractmethod
    def needs_confirmation(self) -> bool:
        pass
