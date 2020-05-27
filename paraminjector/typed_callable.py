import inspect
from dataclasses import dataclass

from cached_property import cached_property
from typing import Any, Callable, Dict, get_type_hints


@dataclass(frozen=True)
class TypedCallable:
    func: Callable

    @cached_property
    def signature(self) -> inspect.Signature:
        return inspect.signature(self.func)

    @cached_property
    def is_coroutine(self) -> bool:
        return inspect.iscoroutinefunction(self.func)

    @cached_property
    def type_hints(self) -> Dict[str, Any]:
        return get_type_hints(self.func)

    @cached_property
    def num_parameters(self) -> int:
        return len(self.signature.parameters)

    @cached_property
    def name(self) -> str:
        return self.func.__name__

    @cached_property
    def description(self) -> str:
        kind = "Coroutine" if self.is_coroutine else "Function"
        return f"{kind} {self.name} with {self.num_parameters} parameters, annotated as {self.type_hints}"

    def __call__(self, *args, **kwargs) -> Any:
        return self.func(*args, **kwargs)
