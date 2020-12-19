from click import ClickException


class NimaException(Exception):
    pass


class NotAProjectDirectory(NimaException, ClickException):
    def __init__(self, directory):
        super(NotAProjectDirectory, self).__init__("Directory {} is not managed by Nima".format(directory))
