import functools
import asyncio

from .common import (
    Decorator,
    Func,
    T
)


def timeout(
    seconds: int | None = None
) -> Decorator:
    """
    Make the function automatically cancel itself if it takes too long to execute.

    Args:
        seconds (int): seconds to timeout

    Example::

        @timeout(seconds=1)
        def my_function():
            pass

        # The function will be cancelled if it takes longer than 1 second
    """

    def decorator(fn: Func) -> Func:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs) -> T:
            coro = fn(*args, **kwargs)

            if seconds is None or seconds <= 0:
                return await coro

            async with asyncio.timeout(seconds):
                return await coro

        return wrapper

    return decorator
