from src.adapters.trash.json_repository import JsonTrashRepository
from src.application.interfaces.terminal import TerminalInterface
from src.application.interfaces.trash import TrashRepository
from src.application.terminal.parser import Parser
from src.constants import CANCELABLE_HISTORY_FILE, HISTORY_FILE, TRASH_FILE
from src.delivery.cli.cli import Cli
from src.application.terminal.terminal import TerminalService
from src.delivery.cli_interface import CliInterface
from src.application.interfaces.history import HistoryRepository
from src.application.interfaces.environment import FileSystemEnvironment
from src.adapters.environment.local_environment import LocalEnvironment

# from src.adapters.commands.in_memory_repostory import InMemoryHistoryRepository
from src.adapters.commands.file_repository import FileHistoryRepository


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    history_repository: HistoryRepository = FileHistoryRepository(HISTORY_FILE)
    cancelable_history_repository: HistoryRepository = FileHistoryRepository(
        CANCELABLE_HISTORY_FILE
    )
    trash_repository: TrashRepository = JsonTrashRepository(TRASH_FILE)
    environment: FileSystemEnvironment = LocalEnvironment()

    parser: Parser = Parser()
    terminal_service: TerminalInterface = TerminalService(
        history_repository,
        cancelable_history_repository,
        trash_repository,
        environment,
        parser,
    )

    cli: CliInterface = Cli(terminal_service)

    cli.serve()


if __name__ == "__main__":
    main()
