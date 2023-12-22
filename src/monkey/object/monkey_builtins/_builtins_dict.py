"""
This module contains the dictionary that maps the name of a built-in function to
the BuiltinObject instance that wraps the functionality.
"""

from monkey.object.builtin_object import BuiltinObject
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_LEN
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_FIRST
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_LAST
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_REST
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_PUSH
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_POP
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_PUTS


BUILTINS_DICT: dict[str, BuiltinObject] = {
    "len": MONKEY_BUILTIN_LEN,
    "first": MONKEY_BUILTIN_FIRST,
    "last": MONKEY_BUILTIN_LAST,
    "rest": MONKEY_BUILTIN_REST,
    "push": MONKEY_BUILTIN_PUSH,
    "pop": MONKEY_BUILTIN_POP,
    "puts": MONKEY_BUILTIN_PUTS,
}
