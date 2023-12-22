"""
This module contains implementation for the BuiltinObject for the `puts` function,
which writes its arguments to sys.stdout.
"""

import sys

from monkey.object.object import Object
from monkey.object.constants import NULL_OBJ


def puts_builtin_impl(*args: Object) -> Object:
    for arg in args:
        sys.stdout.write(f"{arg}\n")

    return NULL_OBJ
