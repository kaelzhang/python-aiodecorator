from typing import Callable
import functools
import asyncio


REPEAT_INFINITY = -1


def repeat(n: int, interval: float = 0.):
    """
    Returns a decorator that repeats the function `fn`
    `n` times with `interval` seconds between each call
    """

    def decorator(fn: Callable):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            result = None

            if n == REPEAT_INFINITY:
                while True:
                    result = await fn(*args, **kwargs)
                    if interval > 0:
                        await asyncio.sleep(interval)

            else:
                for _ in range(n):
                    result = await fn(*args, **kwargs)

                    if interval > 0:
                        # try:
                        await asyncio.sleep(interval)
                        # except asyncio.CancelledError as e:
                            # raise e

            return result
        return wrapper
    return decorator
