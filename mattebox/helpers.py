from time import time


def now_timestamp() -> int:
    """Return current timestamp in milliseconds (ms)."""

    return int(time() * 1000)
