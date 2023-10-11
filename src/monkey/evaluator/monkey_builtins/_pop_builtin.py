"""
This module contains implementation for the BuiltinObject for the `pop` function,
which creates a new container with all the elements of the old container, except
for the last one.

This was not implemented in the book.
"""

import monkey.object as objs


def pop_builtin_impl(*args: objs.Object) -> objs.Object:
    if len(args) != 1:
        message = f"Wrong number of arguments in `pop`: Got {len(args)}, want 1."
        return objs.BuiltinErrorObject(message)

    container = args[0]
    if isinstance(container, objs.StringObject):
        return _pop_from_string(container.value)
    elif isinstance(container, objs.ArrayObject):
        return _pop_from_array(container.elements)
    else:
        container_str = objs.object_type.OBJECT_TYPE_DICT[container.data_type()]
        return objs.BuiltinErrorObject(f"Cannot pop from object of type '{container_str}'")


def _pop_from_string(inner_string: str) -> objs.Object:
    if len(inner_string) == 0:
        return objs.BuiltinErrorObject("The string is empty. Cannot pop an element off it!")

    return objs.StringObject(inner_string[:-1])


def _pop_from_array(elements: list[objs.Object]) -> objs.Object:
    if len(elements) == 0:
        return objs.BuiltinErrorObject("The array is empty. Cannot pop an element off it!")

    new_elements = elements[:-1]
    return objs.ArrayObject(new_elements)
