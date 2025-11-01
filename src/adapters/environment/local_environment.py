from src.application.interfaces.environment import FileSystemEnvironment
import os
import shutil

import src.application.errors.file as errors


class LocalEnvironment(FileSystemEnvironment):
    def read_file(self, file_path: str) -> str:
        with open(file_path, "r") as file:
            return file.read()

    def write_file(self, file_path: str, content: str) -> None:
        with open(file_path, "w") as file:
            file.write(content)

    def write_hex_file(self, file_path: str, content: str) -> None:
        with open(file_path, "wb") as file:
            file.write(bytes.fromhex(content))

    def read_hex_file(self, file_path: str) -> str:
        with open(file_path, "rb") as file:
            return file.read().hex()

    def delete_file(self, file_path: str) -> None:
        if self.exists(file_path):
            with open(file_path, "w") as file:
                file.write("")
        else:
            raise errors.FileNotFoundError(file_path)

    def create_file(self, file_path: str) -> None:
        if not self.exists(file_path):
            with open(file_path, "w") as file:
                file.write("")
        else:
            raise errors.FileAlreadyExistsError(file_path)

    def change_directory(self, directory_path: str) -> None:
        if self.exists(directory_path):
            os.chdir(directory_path)
        else:
            raise errors.DirectoryNotFoundError(directory_path)

    def get_current_directory(self) -> str:
        return os.getcwd()

    def create_directory(self, directory_path: str) -> None:
        if not self.exists(directory_path):
            os.mkdir(directory_path)
        else:
            raise errors.DirectoryAlreadyExistsError(directory_path)

    def delete_directory(self, directory_path: str) -> None:
        if self.exists(directory_path):
            shutil.rmtree(directory_path)
        else:
            raise errors.DirectoryNotFoundError(directory_path)

    def get_directory_list(self, directory_path: str) -> list[str]:
        return os.listdir(directory_path)

    def is_file(self, file_path: str) -> bool:
        return os.path.isfile(file_path)

    def is_directory(self, directory_path: str) -> bool:
        return os.path.isdir(directory_path)

    def exists(self, file_path: str) -> bool:
        return os.path.exists(file_path)

    def copy_directory(self, source_path: str, destination_path: str) -> None:
        shutil.copytree(source_path, destination_path)
