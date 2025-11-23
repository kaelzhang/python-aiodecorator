import pytest
import asyncio

from aiodecorator import timeout


@pytest.mark.asyncio
async def test_timeout():
    @timeout(seconds=1)
    async def my_function():
        await asyncio.sleep(2)
        return 'done'

    with pytest.raises(asyncio.TimeoutError):
        await my_function()


@pytest.mark.asyncio
async def test_timeout_no_seconds():
    @timeout(-1)
    async def my_function():
        await asyncio.sleep(2)
        return 'done'

    assert await my_function() == 'done'
