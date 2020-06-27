from typing import (
    TypeVar,
    Callable,
    Awaitable
)

T = TypeVar('T')


Func = Callable[..., Awaitable[T]]
Decorator = Callable[[Func], Func]
