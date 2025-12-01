import time
import asyncio
import functools
import contextlib

from typing import Literal, Optional

from .common import (
    Decorator,
    Func,
    T
)


class ThrottleCanceledError(asyncio.CancelledError):
    pass


class Throttler:
    __slots__ = (
        'tick',
        'count',
        'task',
        '_canceled_tasks'
    )

    # A tick is a clock tick with interval `interval`
    tick: float
    count: int
    task: Optional[asyncio.Task]
    _canceled_tasks: set

    def __init__(self):
        self.tick = 0.
        self.count = 0
        self.task = None
        self._canceled_tasks = set()

    def set_task(
        self,
        task: asyncio.Task,
    ) -> None:
        self.task = task

    def cancel(self):
        if self.task is not None:
            self._canceled_tasks.add(self.task)  # Remember which task we canceled
            self.task.cancel()
            self.task = None

    @contextlib.contextmanager
    def context(self, task: asyncio.Task):
        try:
            yield
        except asyncio.CancelledError:
            # If this specific task was canceled by the throttler,
            # convert it to ThrottleCanceledError
            if task in self._canceled_tasks:
                # Clear the reference
                self._canceled_tasks.discard(task)
                raise ThrottleCanceledError("Throttler was canceled")
            else:
                # This is an external cancellation, let it propagate
                raise


ThrottleType = Literal['ignore', 'wait', 'replace']


def throttle(
    limit: int,
    interval: float,
    throttle_type: ThrottleType = 'ignore'
) -> Decorator:
    """
    Throttle the function to be called no more than `limit` times
    in every `interval` seconds.

    Args:
        limit: The maximum number of times the function can be called
            in the given interval.
        interval (float | int): The time interval in seconds.
        throttle_type (str): The type of throttle.
        - 'ignore': ignore the function call and return `None` if it exceeds the limit.
        - 'wait': wait for the next tick to execute the function.
        - 'replace': try to cancel the last function call, let it return `None` and execute the current function call.

    Example::

        @throttle(limit=10, interval=1)
        def my_function():
            pass

        # The function will be called at most 10 times per second
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
                    # Just return None of the current call
                    return
                elif throttle_type == 'wait':
                    # Throttle!
                    await asyncio.sleep(sleep)
                elif throttle_type == 'replace':
                    throttler.cancel()

            task = asyncio.create_task(fn(*args, **kwargs))
            throttler.set_task(task)

            try:
                with throttler.context(task):
                    result = await task
            except ThrottleCanceledError:
                return None

            return result

        return wrapper

    return decorator
