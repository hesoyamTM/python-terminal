from abc import ABC, abstractmethod


class CliInterface(ABC):
    """
    Abstract class for CLI interface
    """

    @abstractmethod
    def serve(self) -> None:
        """
        Serves the CLI
        """
        pass
