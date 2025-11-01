from src.application.interfaces.command import Command
from src.application.interfaces.trash import TrashRepository
import os
import shutil
import uuid


class RmCommand(Command):
    _trash_repository: TrashRepository

    def __init__(self, trash_repository: TrashRepository):
        self._trash_repository = trash_repository

    def do(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        # TODO: check length of args
        if len(args) < 1:
            return ""
        if len(args) > 1:
            return ""

        source_path = os.path.normpath(os.path.expanduser(args[0]))

        flag = "".join(flags)

        if os.path.isdir(source_path):
            if "r" in flag:
                if source_path in os.path.normpath(os.getcwd()):
                    # TODO: return error message
                    return ""
                self._add_dir_to_trash(id, source_path)
                shutil.rmtree(source_path)
            else:
                return ""
        elif os.path.isfile(source_path):
            if "f" in flag:
                self._trash_repository.add(
                    id, {source_path: self._get_file_info(source_path)}
                )
                os.remove(source_path)
            else:
                return ""

        return ""

    def undo(self, id: uuid.UUID, args: list[str], flags: list[str]) -> str:
        tree = self._trash_repository.get_by_id(id)

        if tree:
            path, value = tree.popitem()

            if isinstance(value, str):
                with open(path, "wb") as file:
                    file.write(bytes.fromhex(value))
            else:
                os.makedirs(path)
                self._create_file_tree(path, value)

        return ""

    def _create_file_tree(self, path: str, tree: dict) -> None:
        for file_path, file_info in tree.items():
            file_path = os.path.join(path, file_path)

            if isinstance(file_info, str):
                with open(file_path, "wb") as file:
                    file.write(bytes.fromhex(file_info))
            else:
                os.makedirs(file_path)
                self._create_file_tree(file_path, file_info)

    def is_cancelable(self) -> bool:
        return True

    def needs_confirmation(self) -> bool:
        return True

    def _add_dir_to_trash(self, id: uuid.UUID, path: str) -> None:
        path = os.path.normpath(os.path.expanduser(path))
        path = os.path.join(os.getcwd(), path)
        tree: dict = {path: {}}

        self._add_dir_tree(tree[path], path)

        self._trash_repository.add(id, tree)

    def _add_dir_tree(self, tree: dict, path: str) -> None:
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                tree[file] = self._get_file_info(file_path)
            elif os.path.isdir(file_path):
                tree[file] = {}
                self._add_dir_tree(tree[file], file_path)

    def _get_file_info(self, file_path: str) -> str:
        with open(file_path, "rb") as file:
            return file.read().hex()
