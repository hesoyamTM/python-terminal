from unittest.mock import Mock, call
from src.application.commands.mv_command import MvCommand
from src.application.interfaces.environment import FileSystemEnvironment
from src.application.errors.commands import ArgumentError

import uuid
import pytest


def test_mv_happy_path():
    env = Mock(spec=FileSystemEnvironment)
    env.normalize_path.side_effect = ["test1", "test2"]

    command = MvCommand(env)
    id = uuid.uuid4()
    command.do(id, ["test1", "test2"], [])

    env.move.assert_called_once_with("test1", "test2")
    env.normalize_path.assert_has_calls([call(path) for path in ["test1", "test2"]])


def test_mv_wrong_arguments():
    env = Mock(spec=FileSystemEnvironment)

    command = MvCommand(env)
    id = uuid.uuid4()

    with pytest.raises(ArgumentError):
        command.do(id, ["test1", "test2", "test3"], [])

    with pytest.raises(ArgumentError):
        command.do(id, ["test1"], [])


def test_mv_happy_path_undo():
    env = Mock(spec=FileSystemEnvironment)
    env.normalize_path.side_effect = ["test1", "test2"]

    command = MvCommand(env)
    id = uuid.uuid4()
    command.undo(id, ["test1", "test2"], [])

    env.move.assert_called_once_with("test2", "test1")
    env.normalize_path.assert_has_calls([call(path) for path in ["test1", "test2"]])


def test_mv_is_cancelable():
    env = Mock(spec=FileSystemEnvironment)
    command = MvCommand(env)

    assert command.is_cancelable()


def test_mv_needs_confirmation():
    env = Mock(spec=FileSystemEnvironment)
    command = MvCommand(env)

    assert not command.needs_confirmation()
