from functools import wraps
from swissql.manifest import Manifest


class Error(Exception):
    """
    Error class is used to raise exceptions

    """

    def __init__(self, message: str):
        super().__init__()
        self.message = message


def exception_handler():
    def inner_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Error as e:
                print(f"\u001b[31m{Manifest.APP_NAME}: error: {e.message}\u001b[0m")

        return wrapper

    return inner_func
