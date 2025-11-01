from src.application.interfaces.trash import TrashRepository
from typing import Iterator
import uuid
import json


class JsonTrashRepository(TrashRepository):
    _file_path: str

    def __init__(self, file_path: str):
        self._file_path = file_path

    def add(self, id: uuid.UUID, file_tree: dict[str, dict | str]) -> None:
        with open(self._file_path, "a") as file:
            json_file_tree = json.dumps(file_tree)

            file.write(f"{id} {json_file_tree}\n")

    def get(self) -> Iterator[dict[str, dict | str]]:
        with open(self._file_path, "r") as file:
            for line in file:
                line = line.strip()

                if line == "":
                    continue

                _, json_file_tree = line.split(" ", 1)
                file_tree: dict = json.loads(json_file_tree)

                yield file_tree

    def get_by_id(self, id: uuid.UUID) -> dict[str, dict | str] | None:
        with open(self._file_path, "r") as file:
            for line in file:
                line = line.strip()

                file_id, json_file_tree = line.split(" ", 1)

                if file_id == str(id):
                    return json.loads(json_file_tree)

        return None
