from time import time

import logging


_logger = logging.getLogger(__name__)


def _setup_logger():
    _get_logger()


def _get_logger():
    """Sets logging formatter and handler for S2ORC data handling."""
    _logger = logging.getLogger()
    _logger.setLevel(logging.INFO)

    # Log messages once
    _logger.propagate = False

    formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
    handler = logging.FileHandler("logger.log")
    handler.setFormatter(formatter)

    _logger.addHandler(handler)


def timer(func):
    """Prints the execution time of the function object passed."""

    def wrapper(*args, **kwargs):
        start = time()
        output = func(*args, **kwargs)
        end = time()
        delta = end - start
        h, rem = divmod(delta, 3600)
        m, s = divmod(rem, 60)
        _msg = f"RUNTIME: {int(h):0>2}:{int(m):0>2}:{int(s):0>2}"
        _logger.info(_msg)
        return output

    return wrapper


def time_main(func):
    """Prints the execution time of the function object passed."""

    def wrap_main(*args, **kwargs):
        start = time()
        output = func(*args, **kwargs)
        end = time()
        delta = end - start
        h, rem = divmod(delta, 3600)
        m, s = divmod(rem, 60)
        print(f"\n{func.__name__!r} executed in {int(h):0>2}:{int(m):0>2}:{int(s):0>2}")
        return output

    return wrap_main


__all__ = ["timer", "time_main", "_setup_logger"]
