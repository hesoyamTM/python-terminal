from abc import ABC, abstractmethod


class FileSystemEnvironment(ABC):
    @abstractmethod
    def read_file(self, file_path: str) -> str:
        pass

    @abstractmethod
    def write_file(self, file_path: str, content: str) -> None:
        pass

    @abstractmethod
    def write_hex_file(self, file_path: str, content: str) -> None:
        pass

    @abstractmethod
    def read_hex_file(self, file_path: str) -> str:
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> None:
        pass

    @abstractmethod
    def create_file(self, file_path: str) -> None:
        pass

    @abstractmethod
    def change_directory(self, directory_path: str) -> None:
        pass

    @abstractmethod
    def get_current_directory(self) -> str:
        pass

    @abstractmethod
    def create_directory(self, directory_path: str) -> None:
        pass

    @abstractmethod
    def delete_directory(self, directory_path: str) -> None:
        pass

    @abstractmethod
    def get_directory_list(self, directory_path: str) -> list[str]:
        pass

    @abstractmethod
    def is_file(self, file_path: str) -> bool:
        pass

    @abstractmethod
    def is_directory(self, directory_path: str) -> bool:
        pass

    @abstractmethod
    def exists(self, file_path: str) -> bool:
        pass

    @abstractmethod
    def copy_directory(self, source_path: str, destination_path: str) -> None:
        pass
