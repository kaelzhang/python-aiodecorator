import time
import asyncio
import pytest

from aiodecorator import (
    throttle
)


# -----------------------------------------------------
# The throttled function is only called twice a second
@throttle(5, 1)
async def throttled(index: int, now: float):
    return format(time.time() - now, '.0f')
# -----------------------------------------------------


@pytest.mark.asyncio
async def test_throttle():
    now = time.time()

    loop = asyncio.get_running_loop()
    tasks = [
        loop.create_task(throttled(index, now))
        for index in range(20)
    ]

    unpacked = [
        [str(i)] * 5
        for i in range(4)
    ]

    expected = [
        i
        for l in unpacked for i in l
    ]

    assert await asyncio.gather(*tasks) == expected
