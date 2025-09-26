import functools
import asyncio
from typing import Literal
from datetime import datetime, timedelta

from .common import (
    Decorator,
    Func,
    T
)



NaturalInterval = Literal['secondly', 'minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly']


def _seconds_to_next(unit: NaturalInterval) -> float:
    now = datetime.now()

    if unit == 'secondly':
        nxt = (now + timedelta(seconds=1)).replace(microsecond=0)

    elif unit == 'minutely':
        nxt = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)

    elif unit == 'hourly':
        nxt = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

    elif unit == 'daily':
        nxt = (
            now + timedelta(days=1)
        ).replace(hour=0, minute=0, second=0, microsecond=0)

    elif unit == 'weekly':  # assuming week starts on Monday
        days_ahead = 7 - now.weekday()  # 0 = Monday
        nxt = (
            now + timedelta(days=days_ahead)
        ).replace(hour=0, minute=0, second=0, microsecond=0)

    elif unit == 'monthly':
        year = now.year + (now.month // 12)
        month = (now.month % 12) + 1
        nxt = datetime(year, month, 1)

    elif unit == 'yearly':
        nxt = datetime(now.year + 1, 1, 1)

    delta = nxt - now
    return delta.total_seconds()


def schedule_natually(on: NaturalInterval, delay: float = 0.) -> Decorator:
    """
    Returns a decorator that schedules the function `fn`
    to run at natural intervals.

    Args:
        on: `Literal['secondly', 'minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly']` The interval to schedule the function
        delay: `float = 0.` The delay before the function is called

    For example::

        @schedule_natually(on='daily', delay=60)
        async def my_function():
            pass

    The function will be called at 00:01:00 the next day.
    """

    def decorator(fn: Func) -> Func:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs) -> T:
            wait = _seconds_to_next(on) + delay
            await asyncio.sleep(wait)
            return await fn(*args, **kwargs)
        return wrapper
    return decorator
