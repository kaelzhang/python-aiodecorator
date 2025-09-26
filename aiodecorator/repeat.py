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
    `n` times with `interval` seconds between each call

    Args:
        times: `int` The number of times to repeat the function
        interval: `float = 0.` The interval between each call
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
