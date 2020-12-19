import click


class NimaException(Exception):
    pass


class CantAccessFile(NimaException, click.ClickException):
    def __init__(self, message):
        super().__init__("Failed to access file " + message)
