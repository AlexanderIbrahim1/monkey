"""
This module contains implementation for the BuiltinObject for the `len` function,
which calculates the length of an object in the monkey language.
"""

from monkey.object.object import Object
from monkey.object.array_object import ArrayObject
from monkey.object.integer_object import IntegerObject
from monkey.object.error_object import BuiltinErrorObject
from monkey.object.string_object import StringObject


def len_builtin_impl(*args: Object) -> Object:
    if len(args) != 1:
        message = f"Wrong number of arguments in `len`: Got {len(args)}, want 1."
        return BuiltinErrorObject(message)

    arg = args[0]
    if isinstance(arg, StringObject):
        return IntegerObject(len(arg.value))
    elif isinstance(arg, ArrayObject):
        return IntegerObject(len(arg.elements))
    else:
        message = f"Cannot find length of object of type '{arg.data_type()}'"
        return BuiltinErrorObject(message)
