"""
This module contains implementation for the BuiltinObject for the `pop` function,
which creates a new container with all the elements of the old container, except
for the last one.

This was not implemented in the book.
"""

from monkey.object.object_type import OBJECT_TYPE_DICT
from monkey.object.object import Object
from monkey.object.array_object import ArrayObject
from monkey.object.error_object import BuiltinErrorObject
from monkey.object.string_object import StringObject


def pop_builtin_impl(*args: Object) -> Object:
    if len(args) != 1:
        message = f"Wrong number of arguments in `pop`: Got {len(args)}, want 1."
        return BuiltinErrorObject(message)

    container = args[0]
    if isinstance(container, StringObject):
        return _pop_from_string(container.value)
    elif isinstance(container, ArrayObject):
        return _pop_from_array(container.elements)
    else:
        container_str = OBJECT_TYPE_DICT[container.data_type()]
        return BuiltinErrorObject(f"Cannot pop from object of type '{container_str}'")


def _pop_from_string(inner_string: str) -> Object:
    if len(inner_string) == 0:
        return BuiltinErrorObject("The string is empty. Cannot pop an element off it!")

    return StringObject(inner_string[:-1])


def _pop_from_array(elements: list[Object]) -> Object:
    if len(elements) == 0:
        return BuiltinErrorObject("The array is empty. Cannot pop an element off it!")

    new_elements = elements[:-1]
    return ArrayObject(new_elements)
