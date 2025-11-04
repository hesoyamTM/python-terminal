from src.application.interfaces.command import Command
from src.application.interfaces.trash import TrashRepository
from src.application.interfaces.environment import FileSystemEnvironment
from src.application.errors.file import (
    FileError,
    DirectoryIsAFileError,
)
from src.application.errors.commands import ArgumentError
from os import path as os_path
import uuid


class RmCommand(Command):
    """
    rm [-r] <file>
    """

    _trash_repository: TrashRepository

    def __init__(self, trash_repository: TrashRepository, env: FileSystemEnvironment):
        self._trash_repository = trash_repository
        self.env = env

    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        if len(args) != 1:
            raise ArgumentError("rm command requires one argument")

        source_path = self.env.normalize_path(args[0])

        flag = "".join(flags)

        if self.env.is_directory(source_path):
            if "r" in flag:
                if source_path in self.env.get_current_directory():
                    raise FileError("Cannot remove current directory")
                self._add_dir_to_trash(id, source_path)
                self.env.delete_directory(source_path)
            else:
                raise DirectoryIsAFileError(source_path)
        elif self.env.is_file(source_path):
            self._trash_repository.add(
                id, {source_path: self.env.read_hex_file(source_path)}
            )
            self.env.delete_file(source_path)

        return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        tree = self._trash_repository.get_by_id(id)

        if tree:
            path, value = tree.popitem()

            if isinstance(value, str):
                self.env.write_hex_file(path, value)
            else:
                self.env.create_directory(path)
                self._create_file_tree(path, value)

        return ""

    def _create_file_tree(self, path: str, tree: dict) -> None:
        for file_path, file_info in tree.items():
            file_path = os_path.join(path, file_path)

            if isinstance(file_info, str):
                self.env.write_hex_file(file_path, file_info)
            else:
                self.env.create_directory(file_path)
                self._create_file_tree(file_path, file_info)

    def is_cancelable(self) -> bool:
        return True

    def needs_confirmation(self) -> bool:
        return True

    def _add_dir_to_trash(self, id: uuid.UUID, path: str) -> None:
        path = self.env.normalize_path(path)
        if not path.startswith("/"):
            path = os_path.join(self.env.get_current_directory(), path)

        tree: dict = {path: {}}

        self._add_dir_tree(tree[path], path)

        self._trash_repository.add(id, tree)

    def _add_dir_tree(self, tree: dict, path: str) -> None:
        for file in self.env.get_directory_list(path):
            file_path = os_path.join(path, file)
            if self.env.is_file(file_path):
                tree[file] = self.env.read_hex_file(file_path)
            else:
                tree[file] = {}
                self._add_dir_tree(tree[file], file_path)
