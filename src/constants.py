from src.domain.commands.cd_command import CdCommand
from src.domain.commands.cp_command import CpCommand
from src.domain.commands.ls_command import LsCommand
from src.domain.commands.cat_command import CatCommand
from src.domain.commands.mv_command import MvCommand
from src.domain.commands.rm_command import RmCommand
from src.domain.commands.tar_command import TarCommand
from src.domain.commands.zip_command import ZipCommand
from src.domain.commands.unzip_command import UnzipCommand
from src.domain.commands.untar_command import UntarCommand
from src.domain.commands.grep_command import GrepCommand

COMMANDS = {
    "ls": LsCommand(),
    "cd": CdCommand(),
    "cat": CatCommand(),
    "cp": CpCommand(),
    "mv": MvCommand(),
    "rm": RmCommand(),
    "zip": ZipCommand(),
    "unzip": UnzipCommand(),
    "tar": TarCommand(),
    "untar": UntarCommand(),
    "grep": GrepCommand(),
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
