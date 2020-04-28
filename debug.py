import logging
import functools
import typing

logging.root.setLevel(logging.DEBUG)

def debugger(func):
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        logging.debug(f'Entering: {func.__name__}')
        logging.debug(f'args, kwargs: {args, kwargs}')
        value = func(*args, **kwargs)
        logging.debug(f'{func.__name__} returned: {value}')
        return value
    return wrapper_func