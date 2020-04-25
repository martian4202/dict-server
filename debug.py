import logging
import typing

logging.root.setLevel(logging.DEBUG)

class Debugger():
    enabled = True

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        if self.enabled:
            logging.debug(f'Entering: {self.func.__name__}')
            logging.debug(f'args, kwargs: {args, kwargs}')
            logging.debug(f'{self.func.__name__} returned: {self.func(*args, **kwargs)}')
        return self.func(*args, **kwargs)