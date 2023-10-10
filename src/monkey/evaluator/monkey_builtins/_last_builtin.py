"""
This module contains implementation for the BuiltinObject for the `last` function,
which returns the last element of a container in the monkey language.
"""

from typing import Sequence

import monkey.object as objs


def last_builtin_impl(*args: objs.Object) -> objs.Object:
    if len(args) != 1:
        message = f"Wrong number of arguments in `last`: Got {len(args)}, want 1."
        return objs.BuiltinErrorObject(message)

    arg = args[0]
    if isinstance(arg, objs.StringObject):
        return _last_of_string(arg.value)
    elif isinstance(arg, objs.ArrayObject):
        return _last_of_array(arg.elements)
    else:
        message = f"Cannot return last element of object of type '{arg.data_type()}'"
        return objs.BuiltinErrorObject(message)


def _last_of_string(inner_string: str) -> objs.Object:
    if len(inner_string) >= 1:
        return objs.StringObject(inner_string[-1])
    else:
        return objs.OutOfBoundsErrorObject(objs.ObjectType.STRING, 0, len(inner_string))


def _last_of_array(elements: Sequence[objs.Object]) -> objs.Object:
    if len(elements) >= 1:
        return elements[-1]
    else:
        return objs.OutOfBoundsErrorObject(objs.ObjectType.ARRAY, 0, len(elements))
