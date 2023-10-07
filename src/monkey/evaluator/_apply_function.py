from typing import Callable
from typing import Sequence

from monkey.parser import ASTNode
import monkey.object as objs


def apply_function(
    eval_func: Callable[[ASTNode, objs.Environment], objs.Object],
    func: objs.Object,
    args: Sequence[objs.Object],
) -> objs.Object:
    # NOTE: for whatever reason (maybe revealed later) a CallExpression can also take
    # an Identifier as well as a FunctionLiteral
    if isinstance(func, objs.FunctionObject):
        extended_env = _extend_function_environment(func, args)
        evaluated = eval_func(func.body, extended_env)
        return _unwrap_return_value(evaluated)
    elif isinstance(func, objs.BuiltinObject):
        return func.func(*args)
    else:
        return objs.UnknownFunctionErrorObject(func.data_type())


def _extend_function_environment(fnobj: objs.FunctionObject, args: Sequence[objs.Object]) -> objs.Environment:
    env = objs.new_enclosed_environment(fnobj.env)
    for i_identifier, identifier in enumerate(fnobj.parameters):
        env.set(identifier.value, args[i_identifier])

    return env


def _unwrap_return_value(obj: objs.Object) -> objs.Object:
    if isinstance(obj, objs.ReturnObject):
        return obj.value
    else:
        return obj
