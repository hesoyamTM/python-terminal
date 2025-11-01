import pytest
from unittest.mock import Mock
import uuid
from src.application.commands.cp_command import CpCommand
# from src.application.errors.commands import ArgumentError


@pytest.mark.parametrize(
    "source, destination, flag, is_directory",
    [
        ("test.txt", "test2.txt", "", False),
        ("test.txt", "test2.txt", "r", False),
        ("test.txt", "test2.txt", "r", True),
        ("test.txt", "test2.txt", "r", False),
    ],
)
def test_cp_command_happy_path(source, destination, flag, is_directory):
    env = Mock()
    env.normalize_path.effect = [
        source,
        destination,
    ]

    env.is_directory.return_value = is_directory
    env.copy_file.return_value = None

    command = CpCommand(env)
    command.do(uuid.uuid4(), [source, destination], [flag])

    if is_directory:
        env.copy_directory.assert_called_once_with(source, destination)
    else:
        env.copy_file.assert_called_once_with(source, destination)

    env.is_directory.assert_called_once_with(source)
    env.normalize_path.assert_has_calls(
        [
            source,
            destination,
        ]
    )
