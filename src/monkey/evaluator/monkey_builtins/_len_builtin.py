"""
This module contains implementation for the BuiltinObject for the `len` function,
which calculates the length of an object in the monkey language.
"""

import monkey.object as objs


def len_builtin_impl(*args: objs.Object) -> objs.Object:
    if len(args) != 1:
        message = f"Wrong number of arguments in `len`: Got {len(args)}, want 1."
        return objs.BuiltinErrorObject(message)

    arg = args[0]
    if isinstance(arg, objs.StringObject):
        return objs.IntegerObject(len(arg.value))
    elif isinstance(arg, objs.ArrayObject):
        return objs.IntegerObject(len(arg.elements))
    else:
        message = f"Cannot find length of object of type '{arg.data_type()}'"
        return objs.BuiltinErrorObject(message)
