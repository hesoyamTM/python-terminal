import pytest
import uuid
from unittest.mock import Mock
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
    # env.normalize_path.assert_has_calls([call(path) for path in paths])
    # env.get_directory_list.assert_has_calls([call(path) for path in paths])
    # env.get_file_info.assert_has_calls([call(path, paths) for path in paths])
