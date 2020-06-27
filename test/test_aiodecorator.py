import time
import asyncio

from aiodecorator import (
    throttle
)


# The throttled function is only called twice a second
@throttle(5, 1)
async def throttled(index: int, now: float):
    diff = format(time.time() - now, '.0f')
    print(index, f'{diff}s')


def test_main():
    now = time.time()

    async def main():
        loop = asyncio.get_running_loop()
        tasks = [
            loop.create_task(throttled(index, now))
            for index in range(20)
        ]

        await asyncio.wait(tasks)

        await throttled(30, now)

    asyncio.run(main())
