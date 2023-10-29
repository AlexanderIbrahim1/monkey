"""
This module contains implementation for the BuiltinObject for the `first` function,
which returns the first element of a container in the monkey language.
"""

import monkey.object as objs
import monkey.object.object_type as object_type


def first_builtin_impl(*args: objs.Object) -> objs.Object:
    if len(args) != 1:
        message = f"Wrong number of arguments in `first`: Got {len(args)}, want 1."
        return objs.BuiltinErrorObject(message)

    arg = args[0]
    if isinstance(arg, objs.StringObject):
        return _first_of_string(arg.value)
    elif isinstance(arg, objs.ArrayObject):
        return _first_of_array(arg.elements)
    else:
        type_str = object_type.OBJECT_TYPE_DICT[arg.data_type()]
        message = f"Cannot return first element of object of type '{type_str}'"
        return objs.BuiltinErrorObject(message)


def _first_of_string(inner_string: str) -> objs.Object:
    if len(inner_string) >= 1:
        return objs.StringObject(inner_string[0])
    else:
        return objs.OutOfBoundsErrorObject(objs.ObjectType.STRING, 0, len(inner_string))


def _first_of_array(elements: list[objs.Object]) -> objs.Object:
    if len(elements) >= 1:
        return elements[0]
    else:
        return objs.OutOfBoundsErrorObject(objs.ObjectType.ARRAY, 0, len(elements))
