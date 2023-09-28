"""
This module contains code specific to evaluating instances of InfixExpression.
"""

import operator as operator_lib  # already use `operator` as variable in much of the library

from monkey.tokens import Literal
import monkey.tokens.token_types as token_types
import monkey.object as objs


INTEGER_ALGEBRAIC_OPERATION_DICT = {
    token_types.PLUS: operator_lib.add,
    token_types.MINUS: operator_lib.sub,
    token_types.ASTERISK: operator_lib.mul,
    token_types.SLASH: operator_lib.truediv,
}

INTEGER_LOGICAL_OPERATION_DICT = {
    token_types.LT: operator_lib.lt,
    token_types.GT: operator_lib.gt,
    token_types.EQ: operator_lib.eq,
    token_types.NOT_EQ: operator_lib.ne,
}

BOOLEAN_OPERATION_DICT = {
    token_types.EQ: operator_lib.eq,
    token_types.NOT_EQ: operator_lib.ne,
}


def evaluate_infix_expression(operator: Literal, left: objs.Object, right: objs.Object) -> objs.Object:
    if isinstance(left, objs.IntegerObject) and isinstance(right, objs.IntegerObject):
        return _evaluate_integer_infix_expression(operator, left, right)
    if isinstance(left, objs.BooleanObject) and isinstance(right, objs.BooleanObject):
        return _evaluate_boolean_infix_expression(operator, left, right)
    else:
        return objs.NULL_OBJ


def _evaluate_integer_infix_expression(
    operator: Literal, left: objs.IntegerObject, right: objs.IntegerObject
) -> objs.Object:
    if operator in INTEGER_ALGEBRAIC_OPERATION_DICT.keys():
        return _evaluate_integer_algebraic_infix_expression(operator, left, right)
    elif operator in INTEGER_LOGICAL_OPERATION_DICT.keys():
        return _evaluate_integer_logical_infix_expression(operator, left, right)
    else:
        return objs.NULL_OBJ


def _evaluate_boolean_infix_expression(
    operator: Literal, left: objs.BooleanObject, right: objs.BooleanObject
) -> objs.Object:
    if operator in BOOLEAN_OPERATION_DICT.keys():
        operation = BOOLEAN_OPERATION_DICT[operator]
        value = operation(left.value, right.value)
        return objs.BooleanObject(value)
    else:
        return objs.NULL_OBJ


def _evaluate_integer_algebraic_infix_expression(
    operator: Literal, left: objs.IntegerObject, right: objs.IntegerObject
) -> objs.IntegerObject:
    operation = INTEGER_ALGEBRAIC_OPERATION_DICT[operator]
    value = operation(left.value, right.value)
    return objs.IntegerObject(value)


def _evaluate_integer_logical_infix_expression(
    operator: Literal, left: objs.IntegerObject, right: objs.IntegerObject
) -> objs.BooleanObject:
    operation = INTEGER_LOGICAL_OPERATION_DICT[operator]
    value = operation(left.value, right.value)
    return objs.BooleanObject(value)
