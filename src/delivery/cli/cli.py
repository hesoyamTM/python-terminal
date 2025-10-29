from src.application.interfaces.termianal import TerminalInterface
from src.delivery.cli_interface import CliInterface


class Cli(CliInterface):
    """
    CLI class
    """

    _terminal_service: TerminalInterface

    def __init__(self, terminal_service: TerminalInterface):
        """
        Initializes the CLI
        """
        self._terminal_service = terminal_service

    def serve(self) -> None:
        """
        Serves the application
        """

        while True:
            cur_dir = self._terminal_service.get_current_directory()

            data = input(f"{cur_dir}$ ")
            res = self._terminal_service.execute(data)

            if res != "":
                print(res)
