[![](https://travis-ci.org/kaelzhang/python-aiodecorator.svg?branch=master)](https://travis-ci.org/kaelzhang/python-aiodecorator)
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

### schedule_naturally(on, delay: float = 0.)

- **on** `Literal['secondly', 'minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly']`
- **delay** `float = 0.`

Returns a decorator function that schedule a function `fn` to run from the next time moment with a delay `delay`

For example:

```py
@schedule_natually(on: 'daily', delay = 60)
async def run():
    print('hello')

await run()

# It will print 'hello' at 00:01 in the next day
```

### repeat(times: int, interval: float = 0.)

- **times** `int` the number of times to repeat the function
- **interval** `float = 0.` the interval between each call

```py
@repeat(7)
@schedule_naturally(on: 'daily')
@repeat(3)
async def run()
    print('hello')

await run()

# It will schedule a one-week plan, at 00:00:00 each day, it will print 3 'hello'
```

## License

[MIT](LICENSE)
