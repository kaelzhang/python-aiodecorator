import functools
import asyncio

from .common import (
    Decorator,
    Func,
    T
)


REPEAT_INFINITY = -1


def repeat(times: int, interval: float = 0.) -> Decorator:
    """
    Returns a decorator that repeats the function `fn`
    `times` times with `interval` seconds between each call

    Args:
        times: `int` The number of times to repeat the function
        interval: `float = 0.` The interval between each call

    Usage::

        @repeat(3, interval=1)
        async def my_function():
            pass

    The function will be called 3 times with 1 second between each call.
    """

    def decorator(fn: Func) -> Func:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs) -> T:
            result = None

            if times == REPEAT_INFINITY:
                while True:
                    result = await fn(*args, **kwargs)
                    if interval > 0:
                        await asyncio.sleep(interval)

            else:
                for _ in range(times):
                    result = await fn(*args, **kwargs)

                    if interval > 0:
                        await asyncio.sleep(interval)

            return result
        return wrapper
    return decorator
