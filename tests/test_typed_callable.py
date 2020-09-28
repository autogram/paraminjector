import inspect
from functools import wraps
from typing import Optional, Union, get_type_hints

from paraminjector import TypedCallable


class SomeModel:
    pass


def my_func(model: SomeModel, test_int: int = 1, test_none: Optional[str] = None):
    pass


async def my_func_async(model: SomeModel, test_int: int = 1, test_none: Optional[str] = None):
    pass


class TestClass:
    def my_method(self, model: SomeModel, test_int: int = 1, test_none: Optional[str] = None):
        pass

    async def my_method_async(
        self, model: SomeModel, test_int: int = 1, test_none: Optional[str] = None
    ):
        pass


def test_regular_function_properties():
    tc = TypedCallable(my_func)
    assert not tc.is_coroutine
    assert tc.name == "my_func"
    assert tc.num_non_optional_params == 1
    assert tc.num_parameters == 3
    assert tc.type_hints == {
        "model": SomeModel,
        "test_int": int,
        "test_none": Optional[str],
    }


def test_coroutine_function_properties():
    tc = TypedCallable(my_func_async)
    assert tc.is_coroutine
    assert tc.name == "my_func_async"
    assert tc.num_non_optional_params == 1
    assert tc.num_parameters == 3
    assert tc.type_hints == {
        "model": SomeModel,
        "test_int": int,
        "test_none": Optional[str],
    }


def test_regular_method_properties():
    cls = TestClass()
    tc = TypedCallable(cls.my_method)
    assert not tc.is_coroutine
    assert tc.name == "my_method"
    assert tc.num_non_optional_params == 1
    assert tc.num_parameters == 3
    assert tc.type_hints == {
        "model": SomeModel,
        "test_int": int,
        "test_none": Optional[str],
    }


def test_coroutine_method_properties():
    cls = TestClass()
    tc = TypedCallable(cls.my_method_async)
    assert tc.is_coroutine
    assert tc.name == "my_method_async"
    assert tc.num_non_optional_params == 1
    assert tc.num_parameters == 3
    assert tc.type_hints == {
        "model": SomeModel,
        "test_int": int,
        "test_none": Optional[str],
    }


def test_resolve_unions():
    pass


def test_wrapped_decorator_type_hints_return_signature_of_wrapped_function():
    def decorator_with_wraps(func):
        @wraps(func)
        def inner(a: int, b: str):
            func(a, b)

        return inner

    @decorator_with_wraps
    def decorated():
        pass

    tc = TypedCallable(decorated)
    assert tc.name == "decorated"
    assert tc.type_hints == {}


def test_unwrapped_decorator_type_hints_return_signature_of_inner_decorator():
    def decorator_without_wraps(func):
        def inner(a: int, b: str):
            func(a, b)

        return inner

    @decorator_without_wraps
    def decorated():
        pass

    tc = TypedCallable(decorated)
    assert tc.name == "inner"
    assert tc.type_hints == {"a": int, "b": str}


def test_descriptions():
    async def my_thingy(a: Union[int, str], b: Optional[Union[int, str]]):
        pass

    tc = TypedCallable(my_thingy)
    assert (
        tc.description
        == "Asynchronous function my_thingy with signature (a: Union[int, str], b: Union[int, str, NoneType])"
    )
