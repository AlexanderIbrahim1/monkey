"""
This module contains implementation for the BuiltinObject for the `puts` function,
which writes its arguments to sys.stdout.
"""

import sys

import monkey.object as objs


def puts_builtin_impl(*args: objs.Object) -> objs.Object:
    for arg in args:
        sys.stdout.write(f"{arg}\n")

    return objs.NULL_OBJ
