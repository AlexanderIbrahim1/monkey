"""
The compiler uses integers as operands to refer to builtin functions. This means
that for the VM to refer to builtin functions, we need a data structure that maps
non-negative integers to a function (so, a list).

The evaluator can keep using the dict, since that part of the project is allowed
access to less primitive data structures that the compiler and VM.
"""

from monkey.object.builtin_object import BuiltinObject
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_LEN
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_FIRST
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_LAST
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_REST
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_PUSH
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_POP
from monkey.object.monkey_builtins._builtins import MONKEY_BUILTIN_PUTS

INDEX_MONKEY_BUILTIN_LEN = 0
INDEX_MONKEY_BUILTIN_FIRST = 1
INDEX_MONKEY_BUILTIN_LAST = 2
INDEX_MONKEY_BUILTIN_REST = 3
INDEX_MONKEY_BUILTIN_PUSH = 4
INDEX_MONKEY_BUILTIN_POP = 5
INDEX_MONKEY_BUILTIN_PUTS = 6

BUILTINS_LIST: list[BuiltinObject] = [
    MONKEY_BUILTIN_LEN,
    MONKEY_BUILTIN_FIRST,
    MONKEY_BUILTIN_LAST,
    MONKEY_BUILTIN_REST,
    MONKEY_BUILTIN_PUSH,
    MONKEY_BUILTIN_POP,
    MONKEY_BUILTIN_PUTS,
]
