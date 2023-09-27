"""
This module contains the evalute function, which is what evaluates the nodes of
the AST that the parser produced.
"""

from monkey.parser import ASTNode
from monkey.parser import Expression
from monkey.parser import Program
from monkey.parser import Statement
from monkey.tokens import Literal
import monkey.tokens.token_types as token_types
import monkey.parser.expressions as exprs
import monkey.parser.statements as stmts

from monkey.object import Object
import monkey.object as objs


def evaluate(node: ASTNode) -> Object:
    if isinstance(node, Program):
        return _evaluate_program_statements(node)
    elif isinstance(node, Statement):
        return _evaluate_statement(node)
    elif isinstance(node, Expression):
        return _evaluate_expression(node)
    else:
        assert False, "unreachable"


def _evaluate_program_statements(program: Program) -> Object:
    result: Object = objs.NULL_OBJ

    for statement in program:
        result = evaluate(statement)

    return result


def _evaluate_statement(node: Statement) -> Object:
    # Each statement is composed of expressions, and thus the role of this function is
    # to recursively call `evaluate()` again for each statement.
    if isinstance(node, stmts.ExpressionStatement):
        return evaluate(node.value)
    else:
        return objs.NULL_OBJ


def _evaluate_expression(node: Expression) -> Object:
    # For an expression, we either create an Object from the expression directly, or we
    # recursively call `evaluate()` to split the expression up into smaller ones
    if isinstance(node, exprs.IntegerLiteral):
        return objs.IntegerObject(int(node.value))
    if isinstance(node, exprs.BooleanLiteral):
        if node.value == "true":
            return objs.TRUE_BOOL_OBJ
        else:
            return objs.FALSE_BOOL_OBJ
    if isinstance(node, exprs.PrefixExpression):
        argument = evaluate(node.expr)
        return _evaluate_prefix_expression(node.operator, argument)
    else:
        return objs.NULL_OBJ


def _evaluate_prefix_expression(operator: Literal, argument: Object) -> Object:
    if operator == token_types.BANG:
        return _evaluate_band_operator_expression(argument)
    else:
        return objs.NULL_OBJ


def _evaluate_band_operator_expression(argument: Object) -> Object:
    if argument == objs.TRUE_BOOL_OBJ:
        return objs.FALSE_BOOL_OBJ
    elif argument == objs.FALSE_BOOL_OBJ:
        return objs.TRUE_BOOL_OBJ
    elif argument == objs.NULL_OBJ:
        return objs.TRUE_BOOL_OBJ
    else:
        return objs.FALSE_BOOL_OBJ
