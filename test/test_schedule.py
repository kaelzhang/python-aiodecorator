import pytest

from aiodecorator import schedule_naturally

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
