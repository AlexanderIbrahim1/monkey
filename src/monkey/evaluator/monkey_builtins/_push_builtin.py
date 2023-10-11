"""
This module contains implementation for the BuiltinObject for the `push` function,
which creates a new container with all the elements of the old container, and a new
element at the end.
"""

import copy

import monkey.object as objs


def push_builtin_impl(*args: objs.Object) -> objs.Object:
    if len(args) != 2:
        message = f"Wrong number of arguments in `push`: Got {len(args)}, want 2."
        return objs.BuiltinErrorObject(message)

    container = args[0]
    element = args[1]
    if isinstance(container, objs.StringObject) and isinstance(element, objs.StringObject):
        return _push_to_string(container.value, element.value)
    elif isinstance(container, objs.ArrayObject):
        return _push_to_array(container.elements, element)
    else:
        container_str = objs.object_type.OBJECT_TYPE_DICT[container.data_type()]
        element_str = objs.object_type.OBJECT_TYPE_DICT[element.data_type()]
        return objs.BuiltinErrorObject(
            f"Cannot push element of object of type '{element_str}' onto object of type '{container_str}'"
        )


def _push_to_string(inner_string: str, new_char: str) -> objs.Object:
    if len(new_char) != 1:
        return objs.BuiltinErrorObject(
            f"Exactly one character can be pushed onto a string. Found: {len(new_char)}"
        )

    return objs.StringObject(inner_string + new_char)


def _push_to_array(elements: list[objs.Object], new_element: objs.Object) -> objs.Object:
    new_elements_list = copy.deepcopy(elements + [new_element])
    return objs.ArrayObject(new_elements_list)
