import pytest
from unittest.mock import Mock
import uuid

from src.application.commands.cd_command import CdCommand
from src.application.errors.file import DirectoryIsAFileError
from src.application.errors.commands import ArgumentError


@pytest.mark.parametrize(
    "args, expected",
    [
        ("test", "test"),
        ("/test", "/test"),
        ("~/test", "/Users/test"),
        ("~", "/Users/user"),
        ("~/Documents", "/Users/user/Documents"),
        ("..", "/Users/user"),
        ("../Documents", "/Users/user/Documents"),
    ],
)
def test_cd_command_happy_path(args, expected):
    env = Mock()
    env.normalize_path.return_value = expected

    command = CdCommand(env)
    command.do(uuid.uuid4(), [args], [])

    env.change_directory.assert_called_once_with(expected)


def test_cd_wrong_number_of_arguments():
    env = Mock()

    command = CdCommand(env)
    with pytest.raises(ArgumentError):
        command.do(uuid.uuid4(), [], [])
    with pytest.raises(ArgumentError):
        command.do(uuid.uuid4(), ["test", "test"], [])


def test_cd_does_not_exist():
    env = Mock()
    env.normalize_path.return_value = "/Users/user/Documents"
    env.change_directory.side_effect = DirectoryIsAFileError

    command = CdCommand(env)
    with pytest.raises(DirectoryIsAFileError):
        command.do(uuid.uuid4(), ["/Documents"], [])


def test_cd_undo():
    env = Mock()

    command = CdCommand(env)
    assert command.undo(uuid.uuid4(), [], []) == ""


def test_cd_is_cancelable():
    command = CdCommand(Mock())
    assert command.is_cancelable() is False


def test_cd_needs_confirmation():
    command = CdCommand(Mock())
    assert command.needs_confirmation() is False
