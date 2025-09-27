import functools
import asyncio
from typing import Literal, Callable
from datetime import datetime, timedelta

from .common import (
    Decorator,
    Func,
    T
)



NaturalUnit = Literal['secondly', 'minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly']
Weekday = Literal[
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
]


def next_second(
    now: datetime,
    _: Weekday,
    step: int
) -> datetime:
    return (now + timedelta(seconds=1 - step)).replace(microsecond=0)


def next_minute(
    now: datetime,
    _: Weekday,
    step: int
) -> datetime:
    return (now + timedelta(minutes=1 - step)).replace(second=0, microsecond=0)


def next_hour(
    now: datetime,
    _: Weekday,
    step: int
) -> datetime:
    return (
        now + timedelta(hours=1 - step)
    ).replace(minute=0, second=0, microsecond=0)


def next_day(
    now: datetime,
    _: Weekday,
    step: int
) -> datetime:
    return (
        now + timedelta(days=1 - step)
    ).replace(hour=0, minute=0, second=0, microsecond=0)


def next_week(
    now: datetime,
    weekday: Weekday,
    step: int
) -> datetime:
    weekday = weekday.lower()

    # Days left until the next Monday
    days = 7 - now.weekday()  # 0 = Monday

    if weekday == 'tuesday':
        days += 1
    elif weekday == 'wednesday':
        days += 2
    elif weekday == 'thursday':
        days += 3
    elif weekday == 'friday':
        days += 4
    elif weekday == 'saturday':
        days += 5
    elif weekday == 'sunday':
        days += 6

    days = days % 7

    if days == 0:
        days = 7

    return (
        now + timedelta(days=days - step * 7)
    ).replace(hour=0, minute=0, second=0, microsecond=0)


def next_month(
    now: datetime,
    _: Weekday,
    step: int
) -> datetime:
    month = now.month + 1 - step

    return datetime(now.year + (month // 12), month % 12, 1)


def next_year(
    now: datetime,
    _: Weekday,
    step: int
) -> datetime:
    return datetime(now.year + 1 - step, 1, 1)


TypeGetNextTime = Callable[[datetime, Weekday, int], datetime]


class TimeScheduler:
    _get_next_time: TypeGetNextTime

    def __init__(
        self,
        get_next_time: TypeGetNextTime
    ):
        self._get_next_time = get_next_time

    def next_time(
        self,
        now: datetime,
        day: Weekday,
        delay: timedelta,
    ) -> datetime:
        step = 0
        next_time = self._get_next_time(now, day, step) + delay

        while True:
            step += 1
            previous_time = self._get_next_time(now, day, step) + delay

            # if the previous time is now, actually the time already passed
            # so we should return the next time
            if previous_time <= now:
                # If the previous time is before the current time,
                # then the next time is the next time.
                return next_time

            # Otherwise, the next time is the previous time,
            # because we should find the nearest time matching the condition.
            next_time = previous_time


SCHEDULERS = {
    'secondly': TimeScheduler(next_second),
    'minutely': TimeScheduler(next_minute),
    'hourly': TimeScheduler(next_hour),
    'daily': TimeScheduler(next_day),
    'weekly': TimeScheduler(next_week),
    'monthly': TimeScheduler(next_month),
    'yearly': TimeScheduler(next_year),
}

ZERO_TIMEDELTA = timedelta(seconds=0)
DEFAULT_WEEKDAY = 'monday'


def get_time_to_wait(
    now: datetime,
    unit: NaturalUnit,
    weekday: Weekday,
    delay: timedelta
) -> timedelta:
    scheduler = SCHEDULERS[unit]
    next_time = scheduler.next_time(now, weekday, delay)
    return next_time - now


def schedule_naturally(
    unit: NaturalUnit,
    delay: timedelta = ZERO_TIMEDELTA,
    weekday: Weekday = DEFAULT_WEEKDAY
) -> Decorator:
    """
    Returns a decorator that schedules the function `fn`
    to run at natural intervals.

    Args:
        unit: `Literal['secondly', 'minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly']` The unit of the interval to schedule the next function call
        delay: `timedelta = timedelta(seconds=0)` The delay before the function is called
        weekday: `Weekday = 'monday'` The day of the week to schedule the function, only used when `unit` is `weekly`

    For example::

        @schedule_naturally(unit='daily', delay=timedelta(seconds=60))
        async def my_function():
            pass

    The function will be called at 00:01:00 the next day.
    """

    def decorator(fn: Func) -> Func:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs) -> T:
            wait = get_time_to_wait(datetime.now(), unit, weekday, delay)

            await asyncio.sleep(wait.total_seconds())
            return await fn(*args, **kwargs)
        return wrapper
    return decorator
