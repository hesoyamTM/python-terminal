from unittest.mock import Mock
from src.application.commands.tar_command import TarCommand
from src.application.interfaces.environment import FileSystemEnvironment
from src.application.errors.commands import ArgumentError

import pytest
import uuid


@pytest.mark.parametrize("is_directory", [True, False])
def test_tar_happy_path(is_directory: bool):
    env = Mock(spec=FileSystemEnvironment)
    env.normalize_path.side_effect = ["test1", "test2"]

    if is_directory:
        env.is_directory.return_value = True
        env.make_archive.return_value = None
    else:
        env.is_directory.return_value = False
        env.create_directory.return_value = None
        env.copy_file.return_value = None
        env.make_archive.return_value = None
        env.delete_directory.return_value = None

    command = TarCommand(env)

    command.do(uuid.uuid4(), ["test1", "test2"], [])

    env.is_directory.assert_called_once_with("test1")

    if is_directory:
        env.make_archive.assert_called_once_with("test1", "test2", "tar")
    else:
        env.create_directory.assert_called_once_with("test2")
        env.copy_file.assert_called_once_with("test1", "test2")
        env.make_archive.assert_called_once_with("test2", "test2", "tar")
        env.delete_directory.assert_called_once_with("test2")


def test_tar_wrong_arguments():
    env = Mock(spec=FileSystemEnvironment)
    command = TarCommand(env)

    with pytest.raises(ArgumentError):
        command.do(uuid.uuid4(), [], [])


def test_tar_undo():
    env = Mock(spec=FileSystemEnvironment)
    command = TarCommand(env)

    res = command.undo(uuid.uuid4(), [], [])
    assert res == ""


def test_tar_is_cancelable():
    env = Mock(spec=FileSystemEnvironment)
    command = TarCommand(env)

    assert not command.is_cancelable()


def test_tar_needs_confirmation():
    env = Mock(spec=FileSystemEnvironment)
    command = TarCommand(env)

    assert not command.needs_confirmation()
