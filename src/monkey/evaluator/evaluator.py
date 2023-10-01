"""
This module contains the evalute function, which is what evaluates the nodes of
the AST that the parser produced.
"""

from typing import Sequence

from monkey.parser import ASTNode
from monkey.parser import Expression
from monkey.parser import Program
from monkey.parser import Statement
import monkey.parser.expressions as exprs
import monkey.parser.statements as stmts

from monkey.object import Object
from monkey.object import Environment
import monkey.object as objs

from monkey.evaluator._evaluate_prefix_expression import evaluate_prefix_expression
from monkey.evaluator._evaluate_boolean_literal import evaluate_boolean_literal
from monkey.evaluator._evaluate_integer_literal import evaluate_integer_literal
from monkey.evaluator._evaluate_infix_expression import evaluate_infix_expression
from monkey.evaluator._evaluate_if_expression import evaluate_if_expression


def evaluate(node: ASTNode, env: Environment) -> Object:
    if isinstance(node, Program):
        return _evaluate_sequence_of_statements(node.statements, env)
    elif isinstance(node, Statement):
        return _evaluate_statement(node, env)
    elif isinstance(node, Expression):
        return _evaluate_expression(node, env)
    else:
        assert False, f"unreachable; Tried to evaluate something un-evaluable: {node}"


def _evaluate_statement(node: Statement, env: Environment) -> Object:
    # Each statement is composed of expressions, and thus the role of this function is
    # to recursively call `evaluate()` again for each statement.
    if isinstance(node, stmts.ExpressionStatement):
        return evaluate(node.value, env)
    elif isinstance(node, stmts.BlockStatement):
        # return _evaluate_sequence_of_statements(node.statements)
        return _evaluate_block_statement(node, env)
    elif isinstance(node, stmts.ReturnStatement):
        value = evaluate(node.value, env)
        return objs.ReturnObject(value)
    #    elif isinstance(node, stmts.LetStatement):
    #        value = evaluate(node.value)
    #        if value.data_type() == objs.ObjectType.ERROR:
    #            return value
    else:
        stmt_type = type(node)
        assert False, f"unreachable; statement with no known evaluation: {stmt_type}\nFound: {node}"


def _evaluate_sequence_of_statements(statements: Sequence[Statement], env: Environment) -> Object:
    result: Object = objs.NULL_OBJ

    for statement in statements:
        result = evaluate(statement, env)

        if isinstance(result, objs.ReturnObject):
            return result.value
        elif result.data_type() == objs.ObjectType.ERROR:
            return result

    return result


# NOTE: so why can't we use `_evaluate_sequence_of_statements()` for a block statement?
# - the reason is nested return statements
# - consider the following block of code:
# """
# if (10 > 1) {
#     if (10 > 1) {
#         return 123;
#     }
#     return 456;
# };
# """
# - if we used `_evaluate_sequence_of_statements()`, the inner block of code would evaluate
#   directly to `123;`, and this would be equivalent to writing
# """
# if (10 > 1) {
#     123;
#     return 456;
# };
# """
# - but by returning the `ReturnObject` directly instead of the object it wraps, we allow
#   the loop in `_evaluate_sequence_of_statements()` to receive the ReturnObject, and *then*
#   it reaches the `if-statement` within, which returns the wrapped object
def _evaluate_block_statement(block_stmt: stmts.BlockStatement, env: Environment) -> Object:
    result: Object = objs.NULL_OBJ

    for statement in block_stmt.statements:
        result = evaluate(statement, env)

        # NOTE: this is the only difference between this function and `_evaluate_sequence_of_statements`
        if result.data_type() in [objs.ObjectType.RETURN, objs.ObjectType.ERROR]:
            return result

    return result


def _evaluate_expression(node: Expression, env: Environment) -> Object:
    # For an expression, we either create an Object from the expression directly, or we
    # recursively call `evaluate()` to split the expression up into smaller ones
    if isinstance(node, exprs.IntegerLiteral):
        return evaluate_integer_literal(node)
    if isinstance(node, exprs.BooleanLiteral):
        return evaluate_boolean_literal(node)
    if isinstance(node, exprs.PrefixExpression):
        argument = evaluate(node.expr, env)
        operator = node.operator
        return evaluate_prefix_expression(operator, argument)
    if isinstance(node, exprs.InfixExpression):
        left = evaluate(node.left, env)
        right = evaluate(node.right, env)
        operator = node.operator
        return evaluate_infix_expression(operator, left, right)
    if isinstance(node, exprs.IfExpression):
        return evaluate_if_expression(lambda n: evaluate(n, env), node)
    else:
        expr_type = type(node)
        assert False, f"unreachable; expression with no known evaluation: {expr_type}\nFound: {node}"
