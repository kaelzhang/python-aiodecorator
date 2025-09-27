[![](https://github.com/kaelzhang/python-aiodecorator/actions/workflows/python.yml/badge.svg)](https://github.com/kaelzhang/python-aiodecorator/actions/workflows/python.yml)
[![](https://codecov.io/gh/kaelzhang/python-aiodecorator/branch/master/graph/badge.svg)](https://codecov.io/gh/kaelzhang/python-aiodecorator)
[![](https://img.shields.io/pypi/v/aiodecorator.svg)](https://pypi.org/project/aiodecorator/)
[![](https://img.shields.io/pypi/l/aiodecorator.svg)](https://github.com/kaelzhang/python-aiodecorator)

# aiodecorator

Python decorators for asyncio, including

- **throttle**: Throttle a (coroutine) function that return an `Awaitable`
<!-- - limit -->
<!-- - timeout -->

## Install

```sh
$ pip install aiodecorator
```

## Usage

```py
import time
import asyncio

from aiodecorator import (
    throttle
)


async def run(throttle_type):
    now = time.time()

    # -----------------------------------------------------
    # The throttled function is only called twice a second
    @throttle(2, 1, throttle_type)
    async def throttled(index: int):
        diff = format(time.time - now, '.0f')
        print(index, f'{diff}s')
    # -----------------------------------------------------

    loop = asyncio.get_running_loop()
    tasks = [
        loop.create_task(throttled(index))
        for index in range(5)
    ]

    await asyncio.wait(tasks)


asyncio.run(run('wait'))

# Output
# 0 0s
# 1 0s
# 2 1s
# 3 1s
# 4 2s

asyncio.run(run('ignore'))

# Output
# 0 0s
# 1 0s
```

## APIs

### throttle(limit: int, interval: Union[float, int], throttle_type)

- **limit** `int` Maximum number of calls within an `interval`.
- **interval** `Union[int, float]` Timespan for limit in seconds.
- **throttle_type** `Literal['ignore', 'wait'] = 'ignore'`
  - 'ignore': ignore the function call and return `None` if it exceeds the limit.
  - 'wait': wait for the next tick to execute the function.

Returns a decorator function

### schedule_naturally(unit, delay: delay, weekday)

- **unit** `Literal['secondly', 'minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly']`
- **delay** `timedelta = timedelta(seconds=0)`
- **weekday** `Weekday` only used when `unit` is `'weekly'`

Returns a decorator function that schedule a function `fn` to run from the next time moment with a delay `delay`

For example:

```py
@schedule_natually('daily', delay = timedelta(seconds=50))
async def run():
    print('hello')

await run()

# It will print 'hello' at 00:00:50 in the next day
```

```py
@repeat(-1)
@schedule_naturally(
    'weekly',
    delay = timedelta(minutes=5),
    weekday = 'Wednesday'
)
async def run_weekly():
    print('hello')

await run_weekly()

# It will print 'hello' at 00:05 every Wednesday
```

### repeat(times: int, interval: float = 0.)

- **times** `int` the number of times to repeat the function
- **interval** `float = 0.` the interval between each call

```py
@repeat(7)
@schedule_naturally('daily')
@repeat(3)
async def run()
    print('hello')

await run()

# It will schedule a one-week plan, at 00:00:00 each day, it will print 3 'hello'
```

## License

[MIT](LICENSE)
