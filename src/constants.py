from src.domain.commands.cd_command import CdCommand
from src.domain.commands.cp_command import CpCommand
from src.domain.commands.ls_command import LsCommand
from src.domain.commands.cat_command import CatCommand
from src.domain.commands.mv_command import MvCommand
from src.domain.commands.rm_command import RmCommand

COMMANDS = {
    "ls": LsCommand(),
    "cd": CdCommand(),
    "cat": CatCommand(),
    "cp": CpCommand(),
    "mv": MvCommand(),
    "rm": RmCommand(),
}

MONTHS: list[str] = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
