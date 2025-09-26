import time
import asyncio
import functools
from typing import Literal

from .common import (
    Decorator,
    Func,
    T
)


class Throttler:
    __slots__ = (
        'tick',
        'count'
    )

    # A tick is a clock tick with interval `interval`
    tick: float
    count: int

    def __init__(self):
        self.tick = 0.
        self.count = 0


ThrottleType = Literal['ignore', 'wait']


def throttle(
    limit: int,
    interval: float,
    throttle_type: ThrottleType = 'ignore',
) -> Decorator:
    """
    Throttle the function to be called no more than `limit` times
    in `interval` seconds.

    Args:
        limit: The maximum number of times the function can be called
            in the given interval.
        interval (float | int): The time interval in seconds.
        throttle_type (str): The type of throttle.
            - 'ignore': ignore the function call and return `None` if it exceeds the limit.
            - 'wait': wait for the next tick to execute the function.

    Example:
        >>> @throttle(limit=10, interval=1)
        >>> def my_function():
        >>>     pass

        >>> # The function will be called at most 10 times per second
    """

    def decorator(fn: Func) -> Func:
        throttler = Throttler()

        @functools.wraps(fn)
        async def wrapper(*args, **kwargs) -> T:
            now = time.time()

            if now - throttler.tick > interval:
                # Which means the current execution is the first one
                # into the interval span.
                # So we reset the tick and count
                throttler.tick = now
                throttler.count = 1

                # And we could execute the function immediately

            elif throttler.count < limit:
                # It does not exceed the limit of the current tick pointer
                throttler.count += 1

            else:
                # Exceed the limit, move the pointer to the next tick
                throttler.tick += interval
                throttler.count = 1

            sleep = throttler.tick - now

            if sleep > 0:
                if throttle_type == 'ignore':
                    return
                elif throttle_type == 'wait':
                    # Throttle!
                    await asyncio.sleep(sleep)

            return await fn(*args, **kwargs)

        return wrapper

    return decorator
