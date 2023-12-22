"""
This module contains implementation for the BuiltinObject for the `push` function,
which creates a new container with all the elements of the old container, and a new
element at the end.
"""

import copy

from monkey.object.object_type import OBJECT_TYPE_DICT
from monkey.object.object import Object
from monkey.object.array_object import ArrayObject
from monkey.object.error_object import BuiltinErrorObject
from monkey.object.string_object import StringObject


def push_builtin_impl(*args: Object) -> Object:
    if len(args) != 2:
        message = f"Wrong number of arguments in `push`: Got {len(args)}, want 2."
        return BuiltinErrorObject(message)

    container = args[0]
    element = args[1]
    if isinstance(container, StringObject) and isinstance(element, StringObject):
        return _push_to_string(container.value, element.value)
    elif isinstance(container, ArrayObject):
        return _push_to_array(container.elements, element)
    else:
        container_str = OBJECT_TYPE_DICT[container.data_type()]
        element_str = OBJECT_TYPE_DICT[element.data_type()]
        return BuiltinErrorObject(
            f"Cannot push element of object of type '{element_str}' onto object of type '{container_str}'"
        )


def _push_to_string(inner_string: str, new_char: str) -> Object:
    if len(new_char) != 1:
        return BuiltinErrorObject(
            f"Exactly one character can be pushed onto a string. Found: {len(new_char)}"
        )

    return StringObject(inner_string + new_char)


def _push_to_array(elements: list[Object], new_element: Object) -> Object:
    new_elements_list = copy.deepcopy(elements + [new_element])
    return ArrayObject(new_elements_list)
