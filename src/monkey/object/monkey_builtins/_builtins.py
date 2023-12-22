from monkey.object.builtin_object import BuiltinObject

from monkey.object.monkey_builtins._len_builtin import len_builtin_impl
from monkey.object.monkey_builtins._first_builtin import first_builtin_impl
from monkey.object.monkey_builtins._last_builtin import last_builtin_impl
from monkey.object.monkey_builtins._rest_builtin import rest_builtin_impl
from monkey.object.monkey_builtins._push_builtin import push_builtin_impl
from monkey.object.monkey_builtins._pop_builtin import pop_builtin_impl
from monkey.object.monkey_builtins._puts_builtin import puts_builtin_impl

MONKEY_BUILTIN_LEN = BuiltinObject("len", len_builtin_impl)
MONKEY_BUILTIN_FIRST = BuiltinObject("first", first_builtin_impl)
MONKEY_BUILTIN_LAST = BuiltinObject("last", last_builtin_impl)
MONKEY_BUILTIN_REST = BuiltinObject("rest", rest_builtin_impl)
MONKEY_BUILTIN_PUSH = BuiltinObject("push", push_builtin_impl)
MONKEY_BUILTIN_POP = BuiltinObject("pop", pop_builtin_impl)
MONKEY_BUILTIN_PUTS = BuiltinObject("puts", puts_builtin_impl)
