from dataclasses import dataclass

import pytest

from paraminjector import call_with_args
from paraminjector.exceptions import FunctionSignatureInvalid


class AFoo:
    pass


class ABar(AFoo):
    pass


class BFoo:
    pass


def test_simple():
    a = AFoo()
    b = BFoo()

    def callback(a: AFoo, b: BFoo) -> int:
        assert type(a) == AFoo
        assert type(b) == BFoo
        return 1

    res = call_with_args(callback, {type(a): a, type(b): b})
    assert res == 1


def test_with_fixed_positional_args():
    a = AFoo()
    b = BFoo()

    def callback(i: int, a: AFoo, b: BFoo) -> None:
        assert i == 3
        assert type(a) == AFoo
        assert type(b) == BFoo

    call_with_args(callback, {type(a): a, type(b): b}, fixed_pos_args=(3,))


def test_not_enough_fixed_pos_args_raises():
    # noinspection PyUnusedLocal
    def cb(a: int):
        pytest.fail()

    with pytest.raises(FunctionSignatureInvalid) as ex:
        call_with_args(cb, {AFoo: None}, fixed_pos_args=(3, 4))

    assert ex.match(r".*Expected at least 2 parameters.*")


def test_wrong_annotation_for_fixed_pos_arg_raises():
    # noinspection PyUnusedLocal
    def cb(i: str):
        pytest.fail()

    with pytest.raises(FunctionSignatureInvalid) as ex:
        call_with_args(cb, {AFoo: None}, fixed_pos_args=(3,))

    assert ex.match(r".*should always be a supertype.*")


def test_superclass_as_annotation_for_fixed_pos_arg_is_passed():
    def cb(i: AFoo):
        assert isinstance(i, ABar)

    call_with_args(cb, {type(None): None}, fixed_pos_args=(ABar(),))


def test_subclass_as_annotation_for_fixed_pos_arg_raises():
    # noinspection PyUnusedLocal
    def cb(i: ABar):
        pytest.fail()

    with pytest.raises(FunctionSignatureInvalid) as ex:
        call_with_args(cb, {type(None): None}, fixed_pos_args=(AFoo(),))

    assert ex.match(r".*should always be a supertype.*")
