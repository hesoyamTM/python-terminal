from typing import Iterator
from src.domain.commands.command_interface import Command
import os
import stat
import pathlib
import datetime
import pwd
import grp
import src.constants as constants


class LsCommand(Command):
    def do(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        res: str = ""

        if len(args) == 0:
            args = [current_directory]

        if len(args) == 1:
            for file in self.get_files(args[0], flags):
                res += f"{file}\n"
            return res

        for i, path in enumerate(args):
            if i > 0:
                res += "\n"

            res += f"{path}:\n"
            for file in self.get_files(path, flags):
                res += f"{file}\n"

        return res

    def get_files(self, arg: str, flags: list[str]) -> Iterator[str]:
        path = os.path.expanduser(arg)
        # TODO: check if path is a directory
        # if not os.path.exists(path):
        #     return

        flag: str = "".join(flags)

        for file in sorted(os.listdir(path) + ["."] + [".."]):
            if file.startswith(".") and "a" not in flag:
                continue
            if "l" in flag:
                yield self.get_file_info(path, file)
            else:
                yield file

    def get_file_info(self, dir_path: str, file: str) -> str:
        file_path: str = os.path.join(dir_path, file)
        path: pathlib.Path = pathlib.Path(file_path)
        stats: os.stat_result = os.stat(file_path)

        file_type: str
        if path.is_symlink():
            file_type = "l"
        elif path.is_dir():
            file_type = "d"
        else:
            file_type = "-"

        mode: int = stats.st_mode
        permissions = (
            ("r" if mode & stat.S_IRUSR else "-")
            + ("w" if mode & stat.S_IWUSR else "-")
            + ("x" if mode & stat.S_IXUSR else "-")
            + ("r" if mode & stat.S_IRGRP else "-")
            + ("w" if mode & stat.S_IWGRP else "-")
            + ("x" if mode & stat.S_IXGRP else "-")
            + ("r" if mode & stat.S_IROTH else "-")
            + ("w" if mode & stat.S_IWOTH else "-")
            + ("x" if mode & stat.S_IXOTH else "-")
        )

        user: str = pwd.getpwuid(stats.st_uid).pw_name
        group: str = grp.getgrgid(stats.st_gid).gr_name

        last_modified_date: datetime.datetime = datetime.datetime.fromtimestamp(
            stats.st_mtime
        )

        last_modified: str = f"{last_modified_date.day:02d} {constants.MONTHS[last_modified_date.month - 1]}.  {last_modified_date.hour:02d}:{last_modified_date.minute:02d}"

        return f"{file_type}{permissions} {stats.st_nlink} {user}  {group}  {stats.st_size} {last_modified} {file}"

    def undo(self, current_directory: str, args: list[str], flags: list[str]) -> str:
        return ""

    def is_cancelable(self) -> bool:
        return False

    def needs_confirmation(self) -> bool:
        return False
