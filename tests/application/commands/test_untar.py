from unittest.mock import Mock
from src.application.commands.untar_command import UntarCommand
from src.application.interfaces.environment import FileSystemEnvironment
from src.application.errors.commands import ArgumentError

import pytest
import uuid


def test_tar_happy_path():
    env = Mock(spec=FileSystemEnvironment)
    env.normalize_path.return_value = "test1"
    env.get_current_directory.return_value = ""

    command = UntarCommand(env)

    command.do(uuid.uuid4(), ["test1"], [])

    env.extract_archive.assert_called_once_with("test1", "", "tar")


def test_tar_wrong_arguments():
    env = Mock(spec=FileSystemEnvironment)
    command = UntarCommand(env)

    with pytest.raises(ArgumentError):
        command.do(uuid.uuid4(), [], [])


def test_tar_undo():
    env = Mock(spec=FileSystemEnvironment)
    command = UntarCommand(env)

    res = command.undo(uuid.uuid4(), [], [])
    assert res == ""


def test_tar_is_cancelable():
    env = Mock(spec=FileSystemEnvironment)
    command = UntarCommand(env)

    assert not command.is_cancelable()


def test_tar_needs_confirmation():
    env = Mock(spec=FileSystemEnvironment)
    command = UntarCommand(env)

    assert not command.needs_confirmation()
