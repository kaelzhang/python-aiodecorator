import time
import asyncio
import pytest

from aiodecorator import (
    throttle
)


@pytest.mark.asyncio
async def test_throttle():
    # The throttled function is only called twice a second
    @throttle(5, 1, 'wait')
    async def throttled(index: int, now: float):
        return format(time.time() - now, '.0f')

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
        for lst in unpacked for i in lst
    ]

    print('expected:', expected)

    assert await asyncio.gather(*tasks) == expected


@pytest.mark.asyncio
async def test_throttle_ignore():
    @throttle(5, 1, 'ignore')
    async def throttled(index: int, now: float):
        return format(time.time() - now, '.0f')

    now = time.time()

    loop = asyncio.get_running_loop()
    tasks = [
        loop.create_task(throttled(index, now))
        for index in range(20)
    ]

    result = await asyncio.gather(*tasks)

    expected = [
        '0' if i < 5 else None
        for i in range(20)
    ]

    print('result:', result)

    assert result == expected


@pytest.mark.asyncio
async def test_throttle_replace():
    @throttle(5, 1, 'replace', True)
    async def throttled(index: int, now: float):
        return format(time.time() - now, '.0f')

    now = time.time()

    loop = asyncio.get_running_loop()
    tasks = [
        loop.create_task(throttled(index, now))
        for index in range(20)
    ]

    result = await asyncio.gather(*tasks)

    expected = [
        '0' if i == 19 or i < 4 else None
        for i in range(20)
    ]

    print('result:', result)

    assert result == expected


@pytest.mark.asyncio
async def test_throttle_replace_not_swallow_cancel_error():
    @throttle(5, 1, 'replace', False)
    async def throttled(index: int, now: float):
        return format(time.time() - now, '.0f')

    now = time.time()

    errors = []

    async def test_throttled(index: int):
        try:
            result = await throttled(index, now)
            errors.append(False)
            return result
        except asyncio.CancelledError:
            errors.append(True)
            return None

    tasks = [
        asyncio.create_task(test_throttled(index))
        for index in range(20)
    ]

    expected_errors = [
        False if i == 19 or i < 4 else True
        for i in range(20)
    ]

    result = await asyncio.gather(*tasks)

    expected = [
        '0' if i == 19 or i < 4 else None
        for i in range(20)
    ]

    assert result == expected
    assert errors == expected_errors
