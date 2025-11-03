import pytest
import uuid
from unittest.mock import Mock, call
from src.application.commands.ls_command import LsCommand
from src.application.interfaces.environment import FileSystemEnvironment


@pytest.mark.parametrize(
    "paths, flag, expected",
    [
        (["test"], ["l"], "long test\n"),
        (["test"], ["al"], "long test\n"),
        (["test", "test2"], [""], "test:\ntest\n\ntest2:\ntest2"),
        (["test", ".test2"], ["l"], "test:\nlong test\n\n.test2:"),
    ],
)
def test_ls_happy_path(paths, flag, expected):
    env = Mock(spec=FileSystemEnvironment)
    env.normalize_path.side_effect = paths
    env.get_directory_list.side_effect = [[path] for path in paths]
    env.get_file_info.side_effect = ["long " + path for path in paths]

    command = LsCommand(env)
    id = id = uuid.uuid4()

    res = command.do(id, paths, flag)

    print(res)
    print(expected)
    assert res == expected
    env.normalize_path.assert_has_calls([call(path) for path in paths])
    env.get_directory_list.assert_has_calls([call(path) for path in paths])
    # env.get_file_info.assert_has_calls(
    #     [call(path, os.path.join(path, path)) for path in paths]
    # )


def test_ls_empty_args():
    env = Mock(spec=FileSystemEnvironment)
    env.get_current_directory.return_value = "test"
    env.normalize_path.return_value = ["test"]
    env.get_directory_list.return_value = ["test1", "test2"]
    env.get_file_info.side_effect = ["long test1", "long test2"]
    expected = "long test1\nlong test2\n"

    command = LsCommand(env)
    id = id = uuid.uuid4()

    res = command.do(id, [], ["l"])

    print(res)
    print(expected)

    assert res == expected
    env.normalize_path.assert_has_calls([call(path) for path in []])
    env.get_directory_list.assert_has_calls([call(path) for path in []])
    # env.get_file_info.assert_has_calls(
    #     [call(path, os.path.join(path, path)) for path in []]
    # )


def test_ls_undo():
    env = Mock(spec=FileSystemEnvironment)

    command = LsCommand(env)
    id = id = uuid.uuid4()

    assert command.undo(id, [], []) == ""


def test_ls_is_cancelable():
    env = Mock(spec=FileSystemEnvironment)
    command = LsCommand(env)
    assert not command.is_cancelable()


def test_ls_needs_confirmation():
    env = Mock(spec=FileSystemEnvironment)
    command = LsCommand(env)
    assert not command.needs_confirmation()
