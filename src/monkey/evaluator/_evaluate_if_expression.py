"""
This module contains code specific to evaluating instances of IfExpression.
"""

from typing import Callable

from monkey.parser import ASTNode

import monkey.parser.expressions as exprs
import monkey.object as objs


TRUTHY_DICT = {
    objs.TRUE_BOOL_OBJ: True,
    objs.FALSE_BOOL_OBJ: False,
    objs.NULL_OBJ: False,
}


def evaluate_if_expression(
    eval_func: Callable[[ASTNode], objs.Object],
    if_expr: exprs.IfExpression,
) -> objs.Object:
    condition = eval_func(if_expr.condition)

    if _is_truthy(condition):
        return eval_func(if_expr.consequence)
    elif if_expr.alternative is not None:
        return eval_func(if_expr.alternative)
    else:
        # NOTE: this is a proper use of `objs.NULL_OBJ`; an `if-expr` might return nothing!
        return objs.NULL_OBJ


def _is_truthy(obj: objs.Object) -> bool:
    return TRUTHY_DICT.get(obj, True)
