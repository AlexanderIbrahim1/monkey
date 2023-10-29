"""
This module contains implementation for the BuiltinObject for the `rest` function,
which returns all elements after the first element in a container in the monkey language.
"""

import monkey.object as objs
import monkey.object.object_type as object_type


def rest_builtin_impl(*args: objs.Object) -> objs.Object:
    if len(args) != 1:
        message = f"Wrong number of arguments in `rest`: Got {len(args)}, want 1."
        return objs.BuiltinErrorObject(message)

    arg = args[0]
    if isinstance(arg, objs.StringObject):
        return _rest_of_string(arg.value)
    elif isinstance(arg, objs.ArrayObject):
        return _rest_of_array(arg.elements)
    else:
        type_str = object_type.OBJECT_TYPE_DICT[arg.data_type()]
        message = f"Cannot return rest of elements of object of type '{type_str}'"
        return objs.BuiltinErrorObject(message)


def _rest_of_string(inner_string: str) -> objs.Object:
    if len(inner_string) >= 1:
        return objs.StringObject(inner_string[1:])
    else:
        return objs.OutOfBoundsErrorObject(objs.ObjectType.STRING, 0, len(inner_string))


def _rest_of_array(elements: list[objs.Object]) -> objs.Object:
    if len(elements) >= 1:
        return objs.ArrayObject(elements[1:])
    else:
        return objs.OutOfBoundsErrorObject(objs.ObjectType.ARRAY, 0, len(elements))
