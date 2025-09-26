import pytest
import asyncio

from aiodecorator import (
    repeat, REPEAT_INFINITY,
    schedule_naturally
)


@pytest.mark.asyncio
async def test_repeat():
    count = 0

    @repeat(3)
    async def test():
        nonlocal count
        count += 1

        return count

    assert await test() == 3
    assert count == 3


@pytest.mark.asyncio
async def test_repeat_infinity():
    count = 0

    @repeat(REPEAT_INFINITY)
    async def test():
        nonlocal count
        count += 1

        await asyncio.sleep(1)
        return count

    task = asyncio.create_task(test())

    await asyncio.sleep(3)

    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert count == 3


@pytest.mark.asyncio
async def test_repeat_interval():
    count = 0

    @repeat(3, 1)
    async def test():
        nonlocal count
        count += 1
        return count

    task = asyncio.create_task(test())

    await asyncio.sleep(2)

    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert count == 2


@pytest.mark.asyncio
async def test_repeat_interval_infinity():
    count = 0

    @repeat(REPEAT_INFINITY, 1)
    async def test():
        nonlocal count
        count += 1
        return count

    task = asyncio.create_task(test())

    await asyncio.sleep(3)

    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert count == 3


@pytest.mark.asyncio
async def test_schedule_natually():
    count = 0

    @repeat(-1)
    @schedule_naturally('secondly')
    async def test():
        nonlocal count
        count += 1
        return count

    task = asyncio.create_task(test())

    await asyncio.sleep(3)

    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert count == 3
