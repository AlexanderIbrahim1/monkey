"""
This module contains code specific to evaluating instances of PrefixExpression.
"""

from monkey.tokens import Literal
import monkey.tokens.token_types as token_types
import monkey.object as objs


def evaluate_prefix_expression(operator: Literal, argument: objs.Object) -> objs.Object:
    if operator == token_types.BANG:
        return _evaluate_bang_operator_expression(argument)
    elif operator == token_types.MINUS:
        return _evaluate_minus_operator_expression(argument)
    else:
        return objs.NULL_OBJ


def _evaluate_bang_operator_expression(argument: objs.Object) -> objs.Object:
    if argument == objs.TRUE_BOOL_OBJ:
        return objs.FALSE_BOOL_OBJ
    elif argument == objs.FALSE_BOOL_OBJ:
        return objs.TRUE_BOOL_OBJ
    elif argument == objs.NULL_OBJ:
        return objs.TRUE_BOOL_OBJ
    else:
        return objs.FALSE_BOOL_OBJ


def _evaluate_minus_operator_expression(argument: objs.Object) -> objs.Object:
    if not isinstance(argument, objs.IntegerObject):
        return objs.NULL_OBJ

    return objs.IntegerObject(-argument.value)
