import pytest

from aiodecorator import schedule_natually

# Only for testing purposes
# from aiodecorator.schedule import _seconds_to_next


@pytest.mark.asyncio
async def test_schedule_natually():
    count = 0

    @schedule_natually('secondly')
    async def test():
        nonlocal count
        count += 1

        return count

    assert await test() == 1

    assert count == 1
