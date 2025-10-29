from src.application.interfaces.termianal import TerminalInterface
from src.application.terminal.parser import Parser
from src.delivery.cli.cli import Cli
from src.application.terminal.terminal import TerminalService
from src.delivery.cli_interface import CliInterface
from src.domain.commands.repository import HistoryRepository
from src.adapters.commands.in_memory_repostory import InMemoryHistoryRepository


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    history_repository: HistoryRepository = InMemoryHistoryRepository()
    cancelable_history_repository: HistoryRepository = InMemoryHistoryRepository()

    parser: Parser = Parser()
    terminal_service: TerminalInterface = TerminalService(
        history_repository,
        cancelable_history_repository,
        parser,
    )

    cli: CliInterface = Cli(terminal_service)

    cli.serve()


if __name__ == "__main__":
    main()
