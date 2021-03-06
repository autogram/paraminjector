# Paraminjector

This Python library allows you to define a set of parameters and their types which will be available to be passed into
any (third party) user-defined function based on type annotations. This behavior is also referred to as
"argument injection", "autowiring", "magic arguments", and many others.
Most likely you will want to use `paraminjector` as part of a library that expects its users to define functions
with variable parameters that are supposed to be provided automatically if present.

## Installation

`pip install paraminjector`


## Usage

Dynamic injection works as follows:

```python

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

```

Apart from `call_with_args`, there are also `call_with_args_async` for coroutines and `call_with_args_maybe_async`
for cases where you want to allow either a regular function or a coroutine.


