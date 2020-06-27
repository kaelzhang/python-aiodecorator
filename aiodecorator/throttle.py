import time
import asyncio

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


def throttle(
    limit: int,
    interval: float
) -> Decorator:
    def decorator(fn: Func) -> Func:
        throttler = Throttler()

        async def helper(*args, **kwargs) -> T:
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
                # Throttle!
                await asyncio.sleep(sleep)

            return await fn(*args, **kwargs)

        return helper

    return decorator
