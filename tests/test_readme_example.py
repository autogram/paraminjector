from typing import *


class Foo:
    """ Some class defined by your library """


class Bar:
    """ Some other class defined by your library """


# ...

# Your users know that they can use `Foo`, and `Bar` in their callbacks:
def user_defined_callback(i: int, a: Foo, b: Bar) -> None:
    assert i == 3
    assert type(a) is Foo
    assert type(b) is Bar


# Now, in library code:
from paraminjector import call_with_args

# Prepare the possible arguments we want to allow
f = Foo()
b = Bar()

available_args: Dict[Type, object] = {Foo: f, Bar: b}

# We know that the first argument to every callback is always the integer 3 (for sake of example)
fixed_positional_arguments: Tuple = (3,)

# Call the user-defined callback with all known parameters injected as arguments
call_with_args(user_defined_callback, available_args, fixed_positional_arguments)


def test_run():
    call_with_args(user_defined_callback, available_args, fixed_positional_arguments)
