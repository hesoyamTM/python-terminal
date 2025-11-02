import pytest
from unittest.mock import Mock
import uuid

from src.application.commands.cat_command import CatCommand
from src.application.errors.commands import ArgumentError


def test_cat_happy_path():
    env = Mock()
    env.read_file.return_value = "hello world"
    env.normalize_path.return_value = "test.txt"

    command = CatCommand(env)
    result = command.do(uuid.uuid4(), ["test.txt"], [])

    env.read_file.assert_called_once_with("test.txt")
    env.normalize_path.assert_called_once_with("test.txt")
    assert result == "hello world"


def test_cat_wrong_arg_count():
    env = Mock()

    command = CatCommand(env)

    with pytest.raises(ArgumentError):
        command.do(uuid.uuid4(), [], [])

    with pytest.raises(ArgumentError):
        command.do(uuid.uuid4(), ["test.txt", "test2.txt"], [])


def test_cat_undo():
    env = Mock()
    cat_command = CatCommand(env)
    assert cat_command.undo(uuid.uuid4(), [], []) == ""


def test_cat_is_cancelable():
    env = Mock()
    cat_command = CatCommand(env)
    assert not cat_command.is_cancelable()


def test_cat_needs_confirmation():
    env = Mock()
    cat_command = CatCommand(env)
    assert not cat_command.needs_confirmation()
