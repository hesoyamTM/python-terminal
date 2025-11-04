import pytest
import uuid

from unittest.mock import Mock
from src.application.interfaces.trash import TrashRepository
from src.application.interfaces.environment import FileSystemEnvironment
from src.application.commands.rm_command import RmCommand

from src.application.errors.commands import ArgumentError

from src.application.errors.file import DirectoryIsAFileError


def test_rm_file_happy_path():
    env = Mock(spec=FileSystemEnvironment)
    env.is_file.return_value = True
    env.is_directory.return_value = False
    env.normalize_path.return_value = "test.txt"
    env.read_hex_file.return_value = "0123456789abcdef"
    env.delete_file.return_value = None
    trash_repository = Mock(spec=TrashRepository)
    trash_repository.add.return_value = None

    command = RmCommand(trash_repository, env)
    id = uuid.uuid4()
    result = command.do(id, ["test.txt"], [])

    assert result == ""
    env.delete_file.assert_called_once_with("test.txt")
    env.read_hex_file.assert_called_once_with("test.txt")
    env.normalize_path.assert_called_once_with("test.txt")
    env.is_file.assert_called_once_with("test.txt")
    env.is_directory.assert_called_once_with("test.txt")
    trash_repository.add.assert_called_once_with(id, {"test.txt": "0123456789abcdef"})


def test_rm_directory_happy_path():
    env = Mock(spec=FileSystemEnvironment)

    env.is_directory.return_value = True
    env.is_file.side_effect = [
        True,
        True,
        False,
        True,
        True,
    ]
    env.normalize_path.side_effect = [
        "test_folder",
        "test_folder",
        "test_folder/test2.txt",
        "test_folder/test_folder_2/test3.txt",
        "test_folder/test_folder_2/test4.txt",
    ]
    env.read_hex_file.side_effect = [
        "0123456789abcdef_1",
        "0123456789abcdef_2",
        "0123456789abcdef_3",
        "0123456789abcdef_4",
    ]
    env.get_current_directory.return_value = ""
    env.get_directory_list.side_effect = [
        ["test1.txt", "test2.txt", "test_folder_2"],
        ["test3.txt", "test4.txt"],
    ]

    trash_repository = Mock(spec=TrashRepository)

    command = RmCommand(trash_repository, env)
    id = uuid.uuid4()
    result = command.do(id, ["test_folder"], ["r"])

    assert result == ""

    env.delete_directory.assert_called_once_with("test_folder")
    trash_repository.add.assert_called_once_with(
        id,
        {
            "test_folder": {
                "test1.txt": "0123456789abcdef_1",
                "test2.txt": "0123456789abcdef_2",
                "test_folder_2": {
                    "test3.txt": "0123456789abcdef_3",
                    "test4.txt": "0123456789abcdef_4",
                },
            }
        },
    )


def test_rm_wrong_arguments():
    env = Mock(spec=FileSystemEnvironment)
    trash_repository = Mock(spec=TrashRepository)
    command = RmCommand(trash_repository, env)
    id = uuid.uuid4()
    with pytest.raises(ArgumentError):
        command.do(id, [], [])

    with pytest.raises(ArgumentError):
        command.do(id, ["test.txt", "test2.txt"], [])


def test_rm_directory_not_recursive():
    env = Mock(spec=FileSystemEnvironment)
    env.is_directory.return_value = True
    env.normalize_path.return_value = "test_folder"

    trash_repository = Mock(spec=TrashRepository)
    command = RmCommand(trash_repository, env)

    id = uuid.uuid4()
    with pytest.raises(DirectoryIsAFileError):
        command.do(id, ["test_folder"], [])
