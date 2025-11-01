class CommandError(Exception):
    pass


class CommandNotFoundError(CommandError):
    pass


class ArgumentError(CommandError):
    pass
