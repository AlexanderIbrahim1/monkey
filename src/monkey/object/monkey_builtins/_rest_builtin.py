"""
This module contains implementation for the BuiltinObject for the `rest` function,
which returns all elements after the first element in a container in the monkey language.
"""

from monkey.object.object_type import ObjectType
from monkey.object.object_type import OBJECT_TYPE_DICT
from monkey.object.object import Object
from monkey.object.array_object import ArrayObject
from monkey.object.error_object import BuiltinErrorObject
from monkey.object.error_object import OutOfBoundsErrorObject
from monkey.object.string_object import StringObject


def rest_builtin_impl(*args: Object) -> Object:
    if len(args) != 1:
        message = f"Wrong number of arguments in `rest`: Got {len(args)}, want 1."
        return BuiltinErrorObject(message)

    arg = args[0]
    if isinstance(arg, StringObject):
        return _rest_of_string(arg.value)
    elif isinstance(arg, ArrayObject):
        return _rest_of_array(arg.elements)
    else:
        type_str = OBJECT_TYPE_DICT[arg.data_type()]
        message = f"Cannot return rest of elements of object of type '{type_str}'"
        return BuiltinErrorObject(message)


def _rest_of_string(inner_string: str) -> Object:
    if len(inner_string) >= 1:
        return StringObject(inner_string[1:])
    else:
        return OutOfBoundsErrorObject(ObjectType.STRING, 0, len(inner_string))


def _rest_of_array(elements: list[Object]) -> Object:
    if len(elements) >= 1:
        return ArrayObject(elements[1:])
    else:
        return OutOfBoundsErrorObject(ObjectType.ARRAY, 0, len(elements))
