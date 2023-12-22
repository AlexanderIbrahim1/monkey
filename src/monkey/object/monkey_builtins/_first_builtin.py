"""
This module contains implementation for the BuiltinObject for the `first` function,
which returns the first element of a container in the monkey language.
"""

from monkey.object.object_type import ObjectType
from monkey.object.object_type import OBJECT_TYPE_DICT
from monkey.object.object import Object
from monkey.object.array_object import ArrayObject
from monkey.object.error_object import BuiltinErrorObject
from monkey.object.error_object import OutOfBoundsErrorObject
from monkey.object.string_object import StringObject


def first_builtin_impl(*args: Object) -> Object:
    if len(args) != 1:
        message = f"Wrong number of arguments in `first`: Got {len(args)}, want 1."
        return BuiltinErrorObject(message)

    arg = args[0]
    if isinstance(arg, StringObject):
        return _first_of_string(arg.value)
    elif isinstance(arg, ArrayObject):
        return _first_of_array(arg.elements)
    else:
        type_str = OBJECT_TYPE_DICT[arg.data_type()]
        message = f"Cannot return first element of object of type '{type_str}'"
        return BuiltinErrorObject(message)


def _first_of_string(inner_string: str) -> Object:
    if len(inner_string) >= 1:
        return StringObject(inner_string[0])
    else:
        return OutOfBoundsErrorObject(ObjectType.STRING, 0, len(inner_string))


def _first_of_array(elements: list[Object]) -> Object:
    if len(elements) >= 1:
        return elements[0]
    else:
        return OutOfBoundsErrorObject(ObjectType.ARRAY, 0, len(elements))
