import pytest
from unittest.mock import Mock
from src.application.commands.history_command import HistoryCommand
from src.application.errors.commands import ArgumentError
import uuid

from src.application.interfaces.history import HistoryRepository


def test_history_happy_path():
    repo = Mock(spec=HistoryRepository)
    repo.get.return_value = ["test"]
    command = HistoryCommand(repo)
    id = uuid.uuid4()
    res = command.do(id, [], [])

    assert res == "test"

    repo.get.assert_called_once_with()


def test_history_wrong_argument():
    repo = Mock(spec=HistoryRepository)

    command = HistoryCommand(repo)

    id = uuid.uuid4()
    with pytest.raises(ArgumentError):
        command.do(id, ["test"], [])


def test_history_empty_history():
    repo = Mock(spec=HistoryRepository)
    repo.get.return_value = []
    command = HistoryCommand(repo)
    id = uuid.uuid4()
    res = command.do(id, [], [])

    assert res == ""


def test_history_undo():
    repo = Mock(spec=HistoryRepository)
    command = HistoryCommand(repo)
    id = uuid.uuid4()

    assert command.undo(id, [], []) == ""


def test_history_is_cancelable():
    repo = Mock(spec=HistoryRepository)
    command = HistoryCommand(repo)
    assert not command.is_cancelable()


def test_history_needs_confirmation():
    repo = Mock(spec=HistoryRepository)
    command = HistoryCommand(repo)

    assert not command.needs_confirmation()
