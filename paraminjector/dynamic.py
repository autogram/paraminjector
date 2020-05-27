from typing import Any, Callable, Type, Union, Dict, Tuple
from typing import Awaitable

from paraminjector.typed_callable import TypedCallable
from paraminjector._injector import _analyze_signature


async def call_with_args_async():
    """
    Wraps it in an awaitable if it's not
    """
    raise NotImplemented()


def call_with_args(
    func: Callable,
    available_args: Dict[Type, object],
    fixed_pos_args: Tuple = None,
    follow_wrapped: bool = True
) -> Any:
    args = _analyze_signature(
        func=TypedCallable(func),
        available_args=available_args,
        fixed_pos_args=fixed_pos_args,
        follow_wrapped=follow_wrapped,
    )

    if fixed_pos_args:
        return func(*fixed_pos_args, **args)
    else:
        return func(**args)


def call_with_args_maybe_async() -> Union[Any, Awaitable[Any]]:
    raise NotImplemented()
