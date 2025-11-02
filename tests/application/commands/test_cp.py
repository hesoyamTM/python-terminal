import pytest
from unittest.mock import Mock, call
import uuid
from src.application.commands.cp_command import CpCommand
from src.application.errors.file import FileIsADirectoryError
from src.application.errors.commands import ArgumentError


@pytest.mark.parametrize(
    "source, destination, flag, is_directory",
    [
        ("test.txt", "test2.txt", "", False),
        ("test.txt", "test2.txt", "r", False),
        ("test.txt", "test2.txt", "r", True),
    ],
)
def test_cp_command_happy_path(source, destination, flag, is_directory):
    env = Mock()
    env.normalize_path.side_effect = [
        source,
        destination,
    ]

    env.is_directory.return_value = is_directory
    env.copy_file.return_value = None

    command = CpCommand(env)
    command.do(uuid.uuid4(), [source, destination], [flag])

    env.normalize_path.assert_has_calls(
        [
            call(source),
            call(destination),
        ]
    )
    env.is_directory.assert_called_once_with(source)
    if is_directory:
        env.copy_directory.assert_called_once_with(source, destination)
    else:
        env.copy_file.assert_called_once_with(source, destination)


def test_cp_command_wrong_arguments():
    env = Mock()
    env.normalize_path.side_effect = [
        "test.txt",
        "test2.txt",
    ]
    env.is_directory.return_value = False
    env.copy_file.return_value = None

    command = CpCommand(env)
    with pytest.raises(ArgumentError):
        command.do(uuid.uuid4(), ["test.txt"], ["r"])

    with pytest.raises(ArgumentError):
        command.do(uuid.uuid4(), ["test.txt", "test2.txt", "test3.txt"], ["r"])

    assert env.normalize_path.call_count == 0
    assert env.is_directory.call_count == 0
    assert env.copy_file.call_count == 0


def test_cp_command_copy_directory_not_recursive():
    env = Mock()
    env.normalize_path.side_effect = [
        "test",
        "test",
    ]

    env.is_directory.return_value = True
    env.copy_directory.return_value = None

    command = CpCommand(env)
    with pytest.raises(FileIsADirectoryError):
        command.do(uuid.uuid4(), ["test", "test"], [""])

    assert env.normalize_path.call_count == 2
    assert env.is_directory.call_count == 1
    assert env.copy_directory.call_count == 0


@pytest.mark.parametrize(
    "source, destination, flag, is_directory",
    [
        ("test.txt", "test2.txt", "", False),
        ("test.txt", "test2.txt", "r", False),
        ("test.txt", "test2.txt", "r", True),
    ],
)
def test_cp_command_undo_happy_path(source, destination, flag, is_directory):
    env = Mock()
    env.normalize_path.side_effect = [
        destination,
    ]

    env.is_directory.return_value = is_directory
    env.delete_file.return_value = None
    env.delete_directory.return_value = None

    command = CpCommand(env)
    command.undo(uuid.uuid4(), [source, destination], [flag])

    env.normalize_path.assert_has_calls(
        [
            call(destination),
        ]
    )
    if is_directory:
        env.delete_directory.assert_called_once_with(destination)
    else:
        env.delete_file.assert_called_once_with(destination)


def test_cp_command_is_cancelable():
    env = Mock()

    command = CpCommand(env)
    assert command.is_cancelable()


def test_cp_command_needs_confirmation():
    env = Mock()

    command = CpCommand(env)
    assert not command.needs_confirmation()
