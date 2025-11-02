import pytest
from unittest.mock import Mock, call
from src.application.commands.grep_command import GrepCommand
from src.application.interfaces.environment import FileSystemEnvironment
from src.application.errors.commands import ArgumentError
import uuid
import os


@pytest.mark.parametrize(
    "path, pattern, flag, is_dir, expected",
    [
        (
            "test_grep.py",
            "grep",
            "r",
            False,
            "test_grep.py: 1:0: \033[1;31mgrep\033[0m",
        ),
        (
            "test_grep.py",
            "grep",
            "ir",
            False,
            "test_grep.py: 1:0: \033[1;31mgrep\033[0m",
        ),
        (
            "test_grep.py",
            "grep",
            "ri",
            False,
            "test_grep.py: 1:0: \033[1;31mgrep\033[0m",
        ),
        (
            "test_grep.py",
            "grep",
            "i",
            False,
            "test_grep.py: 1:0: \033[1;31mgrep\033[0m",
        ),
        (
            "test_grep.py",
            "GrEp",
            "ri",
            False,
            "test_grep.py: 1:0: \033[1;31mgrep\033[0m",
        ),
    ],
)
def test_grep_file_happy_path(
    path: str, pattern: str, flag: str, is_dir: bool, expected: str
):
    env = Mock(spec=FileSystemEnvironment)
    env.is_directory.return_value = is_dir
    env.read_lines.return_value = ["grep"]
    env.normalize_path.return_value = path

    command = GrepCommand(env)
    id = uuid.uuid4()
    res = command.do(id, [pattern, path], [flag])

    assert res == expected

    env.is_directory.assert_called_once_with(path)
    env.read_lines.assert_called_once_with(path)
    env.normalize_path.assert_called_once_with(path)


@pytest.mark.parametrize(
    "path, pattern, flag, files, lines, expected",
    [
        (
            "test",
            "grep",
            "r",
            ["test_grep.py"],
            [
                ["my test grep", "super test grep"],
            ],
            """test/test_grep.py: 1:8: my test \33[1;31mgrep\33[0m
test/test_grep.py: 2:11: super test \33[1;31mgrep\33[0m""",
        ),
        (
            "test",
            "grep",
            "r",
            [
                "test_grep.py",
                "test_grep2.py",
            ],
            [
                ["my test grep", "super test grep"],
                ["my test grep2", "super test grep2"],
            ],
            """test/test_grep.py: 1:8: my test \33[1;31mgrep\33[0m
test/test_grep.py: 2:11: super test \33[1;31mgrep\33[0m
test/test_grep2.py: 1:8: my test \33[1;31mgrep\33[0m2
test/test_grep2.py: 2:11: super test \33[1;31mgrep\33[0m2""",
        ),
        (
            "test",
            "GREP",
            "ri",
            ["test_grep.py", "test_grep2.py"],
            [
                ["my test grep", "super test grep"],
                ["my test grep2", "super test grep2"],
            ],
            """test/test_grep.py: 1:8: my test \33[1;31mgrep\33[0m
test/test_grep.py: 2:11: super test \33[1;31mgrep\33[0m
test/test_grep2.py: 1:8: my test \33[1;31mgrep\33[0m2
test/test_grep2.py: 2:11: super test \33[1;31mgrep\33[0m2""",
        ),
    ],
)
def test_grep_directory_happy_path(path, pattern, flag, files, lines, expected):
    env = Mock(spec=FileSystemEnvironment)
    env.is_directory.return_value = True
    env.read_lines.side_effect = lines
    env.normalize_path.return_value = path
    env.get_directory_list.return_value = files
    env.is_file.return_value = True

    command = GrepCommand(env)
    id = uuid.uuid4()
    res = command.do(id, [pattern, path], [flag])

    assert res == expected

    env.is_directory.assert_called_once_with(path)
    env.read_lines.assert_has_calls([call(os.path.join(path, file)) for file in files])
    env.normalize_path.assert_called_once_with(path)
    env.get_directory_list.assert_called_once_with(path)
    env.is_file.assert_has_calls([call(os.path.join(path, file)) for file in files])


def test_grep_wrong_arguments():
    env = Mock(spec=FileSystemEnvironment)
    command = GrepCommand(env)
    id = uuid.uuid4()

    with pytest.raises(ArgumentError):
        command.do(id, ["grep", "test_grep.py", "test_grep2.py"], ["r"])

    with pytest.raises(ArgumentError):
        command.do(id, ["grep"], [""])


def test_grep_undo():
    env = Mock(spec=FileSystemEnvironment)
    command = GrepCommand(env)
    id = uuid.uuid4()

    assert command.undo(id, [], []) == ""


def test_grep_is_cancelable():
    env = Mock(spec=FileSystemEnvironment)
    command = GrepCommand(env)

    assert not command.is_cancelable()


def test_grep_needs_confirmation():
    env = Mock(spec=FileSystemEnvironment)
    command = GrepCommand(env)

    assert not command.needs_confirmation()
