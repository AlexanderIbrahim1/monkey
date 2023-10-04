from typing import Callable
from typing import Sequence

from monkey.parser import ASTNode

import monkey.object as objs


def apply_function(
    eval_func: Callable[[ASTNode, objs.Environment], objs.Object],
    fnobj: objs.Object,
    args: Sequence[objs.Object],
) -> objs.Object:
    # NOTE: for whatever reason (maybe revealed later) a CallExpression can also take
    # an Identifier as well as a FunctionLiteral
    if not isinstance(fnobj, objs.FunctionObject):
        return objs.UnknownFunctionErrorObject(fnobj.data_type())

    extended_env = _extend_function_environment(fnobj, args)
    evaluated = eval_func(fnobj.body, extended_env)

    return _unwrap_return_value(evaluated)


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
