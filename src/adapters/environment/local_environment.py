from src.application.interfaces.environment import FileSystemEnvironment
from typing import Iterator
import os
import shutil
import stat
import pathlib
import datetime
import pwd
import grp
import src.constants as constants

import src.application.errors.file as errors


class LocalEnvironment(FileSystemEnvironment):
    def read_file(self, file_path: str) -> str:
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {file_path}")
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {file_path}")

    def write_file(self, file_path: str, content: str) -> None:
        try:
            with open(file_path, "w") as file:
                file.write(content)
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {file_path}")
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {file_path}")

    def write_hex_file(self, file_path: str, content: str) -> None:
        try:
            with open(file_path, "wb") as file:
                file.write(bytes.fromhex(content))
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {file_path}")
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {file_path}")

    def read_hex_file(self, file_path: str) -> str:
        try:
            with open(file_path, "rb") as file:
                return file.read().hex()
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {file_path}")
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {file_path}")

    def delete_file(self, file_path: str) -> None:
        try:
            os.remove(file_path)
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {file_path}")
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {file_path}")
        except IsADirectoryError as e:
            raise errors.DirectoryIsAFileError(f"{e}: {file_path}")

    def create_file(self, file_path: str) -> None:
        if not self.exists(file_path):
            try:
                with open(file_path, "w") as file:
                    file.write("")
            except PermissionError as e:
                raise errors.PermissionError(f"{e}: {file_path}")
        else:
            raise errors.FileAlreadyExistsError(file_path)

    def change_directory(self, directory_path: str) -> None:
        try:
            os.chdir(directory_path)
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {directory_path}")
        except FileNotFoundError as e:
            raise errors.DirectoryNotFoundError(f"{e}: {directory_path}")
        except IsADirectoryError | NotADirectoryError as e:
            raise errors.DirectoryIsAFileError(f"{e}: {directory_path}")

    def get_current_directory(self) -> str:
        return os.getcwd()

    def create_directory(self, directory_path: str) -> None:
        if not self.exists(directory_path):
            try:
                os.mkdir(directory_path)
            except PermissionError as e:
                raise errors.PermissionError(f"{e}: {directory_path}")
            except FileNotFoundError as e:
                raise errors.FileNotFoundError(f"{e}: {directory_path}")
            except FileExistsError as e:
                raise errors.FileAlreadyExistsError(f"{e}: {directory_path}")
            except IsADirectoryError | NotADirectoryError as e:
                raise errors.DirectoryIsAFileError(f"{e}: {directory_path}")
        else:
            raise errors.DirectoryAlreadyExistsError(directory_path)

    def delete_directory(self, directory_path: str) -> None:
        if self.exists(directory_path):
            try:
                shutil.rmtree(directory_path)
            except PermissionError as e:
                raise errors.PermissionError(f"{e}: {directory_path}")
            except FileNotFoundError as e:
                raise errors.FileNotFoundError(f"{e}: {directory_path}")
        else:
            raise errors.DirectoryNotFoundError(directory_path)

    def get_directory_list(self, directory_path: str) -> list[str]:
        try:
            return os.listdir(directory_path)
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {directory_path}")
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {directory_path}")
        except IsADirectoryError | NotADirectoryError as e:
            raise errors.DirectoryIsAFileError(f"{e}: {directory_path}")

    def is_file(self, file_path: str) -> bool:
        try:
            return os.path.isfile(file_path)
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {file_path}")
        except IsADirectoryError as e:
            raise errors.FileIsADirectoryError(f"{e}: {file_path}")

    def is_directory(self, directory_path: str) -> bool:
        try:
            return os.path.isdir(directory_path)
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {directory_path}")
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {directory_path}")

    def exists(self, file_path: str) -> bool:
        try:
            return os.path.exists(file_path)
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {file_path}")
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {file_path}")

    def copy_directory(self, source_path: str, destination_path: str) -> None:
        try:
            shutil.copytree(source_path, destination_path)
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {source_path} or {destination_path}")
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {source_path} or {destination_path}")
        except IsADirectoryError as e:
            raise errors.DirectoryIsAFileError(
                f"{e}: {source_path} or {destination_path}"
            )
        except FileExistsError as e:
            raise errors.FileAlreadyExistsError(
                f"{e}: {source_path} or {destination_path}"
            )

    def copy_file(self, source_path: str, destination_path: str) -> None:
        try:
            shutil.copy(source_path, destination_path)
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {source_path} or {destination_path}")
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {source_path} or {destination_path}")
        except IsADirectoryError as e:
            raise errors.FileIsADirectoryError(
                f"{e}: {source_path} or {destination_path}"
            )
        except FileExistsError as e:
            raise errors.FileAlreadyExistsError(
                f"{e}: {source_path} or {destination_path}"
            )
        except NotADirectoryError as e:
            raise errors.FileIsADirectoryError(
                f"{e}: {source_path} or {destination_path}"
            )

    def normalize_path(self, path: str) -> str:
        return os.path.normpath(path)

    def read_lines(self, file_path: str) -> Iterator[str]:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    yield line
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {file_path}")
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {file_path}")
        except IsADirectoryError as e:
            raise errors.FileIsADirectoryError(f"{e}: {file_path}")
        except NotADirectoryError as e:
            raise errors.FileIsADirectoryError(f"{e}: {file_path}")

    def get_file_info(self, dir_path: str, file: str) -> str:
        try:
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

        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {dir_path} or {file}")
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {dir_path} or {file}")
        except NotADirectoryError as e:
            raise errors.FileIsADirectoryError(f"{e}: {dir_path} or {file}")

    def move(self, source_path: str, destination_path: str) -> None:
        try:
            if os.path.exists(destination_path):
                shutil.move(source_path, destination_path)
            else:
                raise errors.FileAlreadyExistsError(
                    f"File already exists: {destination_path}"
                )
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {source_path} or {destination_path}")
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {source_path} or {destination_path}")
        except IsADirectoryError as e:
            raise errors.FileIsADirectoryError(
                f"{e}: {source_path} or {destination_path}"
            )
        except FileExistsError as e:
            raise errors.FileAlreadyExistsError(
                f"{e}: {source_path} or {destination_path}"
            )

    def make_archive(
        self, source_path: str, destination_path: str, format: str
    ) -> None:
        try:
            shutil.make_archive(destination_path, format, source_path)
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {source_path} or {destination_path}")
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {source_path} or {destination_path}")
        except FileExistsError as e:
            raise errors.FileAlreadyExistsError(
                f"{e}: {source_path} or {destination_path}"
            )

    def extract_archive(
        self, source_path: str, destination_path: str, format: str
    ) -> None:
        try:
            shutil.unpack_archive(source_path, destination_path)
        except FileNotFoundError as e:
            raise errors.FileNotFoundError(f"{e}: {source_path} or {destination_path}")
        except PermissionError as e:
            raise errors.PermissionError(f"{e}: {source_path} or {destination_path}")
        except FileExistsError as e:
            raise errors.FileAlreadyExistsError(
                f"{e}: {source_path} or {destination_path}"
            )
