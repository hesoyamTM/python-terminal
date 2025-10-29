from abc import ABC, abstractmethod


class TerminalInterface(ABC):
    """
    Executes commands
    """

    @abstractmethod
    def execute(self, command: str) -> str:
        """
        Executes command
        """
        pass

    @abstractmethod
    def get_current_directory(self) -> str:
        """
        Returns current directory
        """
        pass
