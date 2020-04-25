import logging
import functools
import typing

logging.root.setLevel(logging.DEBUG)

def debugger(func):
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        logging.debug(f'Entering: {func.__name__}')
        logging.debug(f'args, kwargs: {args, kwargs}')
        logging.debug(f'{func.__name__} returned: {func(*args, **kwargs)}')
        return func(*args, **kwargs)
    return wrapper_func