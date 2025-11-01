class FileError(Exception):
    pass


class FileNotFoundError(FileError):
    pass


class FileAlreadyExistsError(FileError):
    pass


class FileIsADirectoryError(FileError):
    pass


class DirectoryError(Exception):
    pass


class DirectoryNotFoundError(DirectoryError):
    pass


class DirectoryAlreadyExistsError(DirectoryError):
    pass


class DirectoryIsAFileError(DirectoryError):
    pass


class PermissionError(Exception):
    pass
