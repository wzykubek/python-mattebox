from time import time


def now_timestamp() -> int:
    return int(time() * 1000)
