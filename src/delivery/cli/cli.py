from src.application.interfaces.terminal import TerminalInterface
from src.delivery.cli_interface import CliInterface

import src.application.errors.commands as commands_errors
import src.application.errors.file as file_errors
from loguru import logger


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
        logger.add(sink="shell.log", level="INFO")
        logger.remove(0)

    def serve(self) -> None:
        """
        Serves the application
        """

        while True:
            cur_dir = self._terminal_service.get_current_directory()

            data = input(f"{cur_dir}$ ")
            logger.info(data)

            if self._terminal_service.needs_confirmation(data):
                choice = input("Are you sure? [y/n] ")

                while choice not in ["y", "n"]:
                    if choice.lower() != "y":
                        continue

                    choice = input("Are you sure? [y/n] ")

            try:
                res = self._terminal_service.execute(data)

                if res != "":
                    print(res)

            except commands_errors.CommandNotFoundError as e:
                logger.error(e)
                print("Command not found")

            except commands_errors.ArgumentError as e:
                logger.error(e)
                print("{e}")

            except file_errors.FileNotFoundError as e:
                logger.error(e)
                print("File not found")

            except file_errors.FileAlreadyExistsError as e:
                logger.error(e)
                print("File already exists")

            except file_errors.FileIsADirectoryError as e:
                logger.error(e)
                print("File is a directory")

            except file_errors.DirectoryNotFoundError as e:
                logger.error(e)
                print("Directory not found")

            except file_errors.DirectoryAlreadyExistsError as e:
                logger.error(e)
                print("Directory already exists")

            except file_errors.DirectoryIsAFileError as e:
                logger.error(e)
                print("Directory is a file")

            except file_errors.PermissionError as e:
                logger.error(e)
                print("Permission denied")
