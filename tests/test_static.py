import pytest
from typing import Optional
from paraminjector import ParamInjector


class AFoo:
    pass


class ABar(AFoo):
    pass


class BFoo:
    pass


def test_initialization():
    ParamInjector(dict())


def test_all_simple_parameters_injected_into_callback():
    # noinspection PyUnusedLocal
    async def callback(a: AFoo, b: BFoo) -> None:
        pass

    references = {AFoo: AFoo(), BFoo: BFoo()}
    inj = ParamInjector(references)
    kwargs = inj.map_kwargs(callback)

    assert kwargs.get("a") == references[AFoo]
    assert kwargs.get("b") == references[BFoo]


def test_extra_nondefault_args_raises():
    # noinspection PyUnusedLocal
    async def callback(b: BFoo, c: str) -> None:
        assert b is not None
        assert c is not None

    references = {BFoo: BFoo()}
    inj = ParamInjector(references)

    with pytest.raises(ValueError):
        assert inj.map_kwargs(callback)


def test_extra_default_kwargs_param_ignored():
    # noinspection PyUnusedLocal
    async def callback(b: BFoo, c: str = "") -> None:
        pass

    references = {BFoo: BFoo()}
    inj = ParamInjector(references)
    kwargs = inj.map_kwargs(callback)

    assert kwargs.get("b") == references[BFoo]
    assert "c" not in kwargs


def test_extra_none_default_kwargs_param_ignored():
    # noinspection PyUnusedLocal
    async def callback(b: BFoo, c: str = None) -> None:
        pass

    references = {BFoo: BFoo()}
    inj = ParamInjector(references)
    kwargs = inj.map_kwargs(callback)

    assert kwargs.get("b") == references[BFoo]
    assert "c" not in kwargs


def test_covariant_arg_injected():
    # noinspection PyUnusedLocal
    async def callback(a: AFoo) -> None:
        pass

    references = {ABar: ABar()}
    inj = ParamInjector(references)
    kwargs = inj.map_kwargs(callback)

    assert kwargs.get("a") == references[ABar]


def test_contravariant_arg_raises():
    # noinspection PyUnusedLocal
    async def callback(a: ABar, b: BFoo) -> None:
        pass

    references = {type(AFoo): AFoo(), type(BFoo): BFoo()}
    inj = ParamInjector(references)

    with pytest.raises(ValueError):
        kwargs = inj.map_kwargs(callback)
