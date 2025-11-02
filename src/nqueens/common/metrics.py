from __future__ import annotations
import time
from contextlib import contextmanager
from typing import Callable, Tuple, Any

@contextmanager
def timer():
    """
    Context manager to measure elapsed time.
    Usage:
        with timer() as t:
            ... code ...
        elapsed = t()
    """
    t0 = time.perf_counter()
    yield lambda: (time.perf_counter() - t0)


class Timer:
    """
    Simple reusable timer class.
    Example:
        with Timer() as T:
            ... code ...
        print(T.elapsed)
    """
    def __enter__(self):
        self._t0 = time.perf_counter()
        self.elapsed = 0.0
        return self

    def __exit__(self, *exc):
        self.elapsed = time.perf_counter() - self._t0


def timeit(fn: Callable[..., Any], *args, **kwargs) -> Tuple[Any, float]:
    """
    Execute a function and return (result, elapsed_time_in_seconds).
    """
    t0 = time.perf_counter()
    out = fn(*args, **kwargs)
    dt = time.perf_counter() - t0
    return out, dt