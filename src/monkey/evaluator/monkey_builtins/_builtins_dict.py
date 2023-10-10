"""
This module contains the dictionary that maps the name of a built-in function to
the BuiltinObject instance that wraps the functionality.
"""

import monkey.object as objs

from monkey.evaluator.monkey_builtins._len_builtin import len_builtin_impl
from monkey.evaluator.monkey_builtins._first_builtin import first_builtin_impl

# TODO: after I get this working, check if it should be `Literal` instead of `str`
BUILTINS_DICT: dict[str, objs.BuiltinObject] = {
    "len": objs.BuiltinObject("len", len_builtin_impl),
    "first": objs.BuiltinObject("first", first_builtin_impl),
}
