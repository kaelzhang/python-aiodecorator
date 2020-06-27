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

now = time.time()


# The throttled function is only called twice a second
@throttle(2, 1)
async def throttled(index: int):
    diff = format(time.time - now, '.0f')
    print(index, f'{diff}s')


async def main():
    loop = asyncio.get_running_loop()
    tasks = [
        loop.create_task(throttled(index))
        for index in range(5)
    ]

    await asyncio.wait(tasks)


asyncio.run(main())

# Output
# 0 0s
# 1 0s
# 2 1s
# 3 1s
# 4 2s
```

## APIs

### throttle(limit: int, interval: Union[float, int])

- **limit** `int` Maximum number of calls within an `interval`.
- **interval** `Union[int, float]` Timespan for limit in seconds.

Returns a decorator function

## License

[MIT](LICENSE)
