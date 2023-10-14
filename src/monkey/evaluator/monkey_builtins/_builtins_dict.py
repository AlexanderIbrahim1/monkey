"""
This module contains the dictionary that maps the name of a built-in function to
the BuiltinObject instance that wraps the functionality.
"""

import monkey.object as objs

from monkey.evaluator.monkey_builtins._len_builtin import len_builtin_impl
from monkey.evaluator.monkey_builtins._first_builtin import first_builtin_impl
from monkey.evaluator.monkey_builtins._last_builtin import last_builtin_impl
from monkey.evaluator.monkey_builtins._rest_builtin import rest_builtin_impl
from monkey.evaluator.monkey_builtins._push_builtin import push_builtin_impl
from monkey.evaluator.monkey_builtins._pop_builtin import pop_builtin_impl
from monkey.evaluator.monkey_builtins._puts_builtin import puts_builtin_impl

# TODO: after I get this working, check if it should be `Literal` instead of `str`
BUILTINS_DICT: dict[str, objs.BuiltinObject] = {
    "len": objs.BuiltinObject("len", len_builtin_impl),
    "first": objs.BuiltinObject("first", first_builtin_impl),
    "last": objs.BuiltinObject("last", last_builtin_impl),
    "rest": objs.BuiltinObject("rest", rest_builtin_impl),
    "push": objs.BuiltinObject("push", push_builtin_impl),
    "pop": objs.BuiltinObject("pop", pop_builtin_impl),
    "puts": objs.BuiltinObject("puts", puts_builtin_impl),
}
