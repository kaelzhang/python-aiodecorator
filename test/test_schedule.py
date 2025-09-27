import pytest
from datetime import datetime, timedelta

from aiodecorator import schedule_naturally
from aiodecorator.schedule import (
    get_time_to_wait,
    DEFAULT_WEEKDAY,
    ZERO_TIMEDELTA,
)

# Only for testing purposes
# from aiodecorator.schedule import _seconds_to_next


@pytest.mark.asyncio
async def test_schedule_naturally():
    count = 0

    @schedule_naturally('secondly')
    async def test():
        nonlocal count
        count += 1

        return count

    assert await test() == 1

    assert count == 1


def test_get_time_to_wait():
    cases = [
        (
            # now
            datetime(2025, 1, 1, 0, 0, 0, 50),
            # unit
            'secondly',
            # weekday
            DEFAULT_WEEKDAY,
            # delay
            timedelta(seconds=1),
            # wait
            timedelta(microseconds=1e6 - 50)
        ),
        (
            datetime(2025, 1, 1, 0, 0, 0, 50),
            'minutely',
            DEFAULT_WEEKDAY,
            timedelta(seconds=20),
            timedelta(seconds=19, microseconds=1e6 - 50)
        ),
        (
            datetime(2025, 1, 1, 0, 0, 0, 50),
            'minutely',
            DEFAULT_WEEKDAY,
            timedelta(seconds=61),
            # There will be a next time slot very soon
            timedelta(microseconds=1e6 - 50)
        ),
        (
            datetime(2025, 1, 1, 0, 1, 0),
            'hourly',
            DEFAULT_WEEKDAY,
            ZERO_TIMEDELTA,
            timedelta(minutes=59)
        ),
        (
            datetime(2025, 1, 1, 0, 0, 0),
            'daily',
            DEFAULT_WEEKDAY,
            ZERO_TIMEDELTA,
            timedelta(hours=24)
        ),
        (
            datetime(2025, 9, 22, 0, 0, 0),
            'weekly',
            DEFAULT_WEEKDAY,
            ZERO_TIMEDELTA,
            timedelta(days=7)
        ),
        (
            datetime(2025, 9, 22, 0, 0, 0),
            'weekly',
            'tuesday',
            ZERO_TIMEDELTA,
            timedelta(days=1)
        ),
        (
            datetime(2025, 9, 22, 0, 0, 0),
            'weekly',
            'wednesday',
            ZERO_TIMEDELTA,
            timedelta(days=2)
        ),
        (
            datetime(2025, 9, 22, 0, 0, 0),
            'weekly',
            'thursday',
            ZERO_TIMEDELTA,
            timedelta(days=3)
        ),
        (
            datetime(2025, 9, 22, 0, 0, 0),
            'weekly',
            'friday',
            ZERO_TIMEDELTA,
            timedelta(days=4)
        ),
        (
            datetime(2025, 9, 22, 0, 0, 0),
            'weekly',
            'saturday',
            ZERO_TIMEDELTA,
            timedelta(days=5)
        ),
        (
            datetime(2025, 9, 22, 0, 0, 0),
            'weekly',
            'sunday',
            ZERO_TIMEDELTA,
            timedelta(days=6)
        ),
        (
            datetime(2025, 9, 22, 0, 0, 0),
            'monthly',
            DEFAULT_WEEKDAY,
            ZERO_TIMEDELTA,
            timedelta(days=9)
        ),
        (
            datetime(2025, 9, 22, 0, 0, 0),
            'yearly',
            DEFAULT_WEEKDAY,
            timedelta(days=265),
            timedelta(days=1)
        ),
    ]

    index = 0

    for now, unit, weekday, delay, expected in cases:
        assert get_time_to_wait(
            now, unit, weekday, delay
        ) == expected, f'Case {index} failed'
        index += 1
