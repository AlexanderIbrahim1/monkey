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

from monkey.evaluator._apply_function import apply_function
from monkey.evaluator._evaluate_boolean_literal import evaluate_boolean_literal
from monkey.evaluator._evaluate_identifier import evaluate_identifier
from monkey.evaluator._evaluate_integer_literal import evaluate_integer_literal
from monkey.evaluator._evaluate_infix_expression import evaluate_infix_expression
from monkey.evaluator._evaluate_if_expression import evaluate_if_expression
from monkey.evaluator._evaluate_prefix_expression import evaluate_prefix_expression
from monkey.evaluator._evaluate_string_literal import evaluate_string_literal


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
        return _evaluate_block_statement(node, env)
    elif isinstance(node, stmts.ReturnStatement):
        value = evaluate(node.value, env)
        if objs.is_error_object(value):
            return value
        return objs.ReturnObject(value)
    elif isinstance(node, stmts.LetStatement):
        value = evaluate(node.value, env)
        if objs.is_error_object(value):
            return value
        identifier_name = node.name.value
        env.set(identifier_name, value)
        return objs.NULL_OBJ  # let statements shouldn't return anything?
    else:
        stmt_type = type(node)
        assert False, f"unreachable; statement with no known evaluation: {stmt_type}\nFound: {node}"


def _evaluate_sequence_of_statements(statements: Sequence[Statement], env: Environment) -> Object:
    result: Object = objs.NULL_OBJ

    for statement in statements:
        result = evaluate(statement, env)

        if isinstance(result, objs.ReturnObject):
            return result.value
        elif objs.is_error_object(result):
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
    elif isinstance(node, exprs.BooleanLiteral):
        return evaluate_boolean_literal(node)
    elif isinstance(node, exprs.StringLiteral):
        return evaluate_string_literal(node)
    elif isinstance(node, exprs.PrefixExpression):
        argument = evaluate(node.expr, env)
        if objs.is_error_object(argument):
            return argument
        operator = node.operator
        return evaluate_prefix_expression(operator, argument)
    elif isinstance(node, exprs.InfixExpression):
        left = evaluate(node.left, env)
        if objs.is_error_object(left):
            return left
        right = evaluate(node.right, env)
        if objs.is_error_object(right):
            return right
        operator = node.operator
        return evaluate_infix_expression(operator, left, right)
    elif isinstance(node, exprs.IfExpression):
        return evaluate_if_expression(lambda n: evaluate(n, env), node)
    elif isinstance(node, exprs.Identifier):
        return evaluate_identifier(node, env)
    elif isinstance(node, exprs.FunctionLiteral):
        return objs.FunctionObject(node.parameters, node.body, env)
    elif isinstance(node, exprs.CallExpression):
        func = evaluate(node.function, env)
        if objs.is_error_object(func):
            return func
        arguments: list[Object] = _evaluate_sequence_of_expressions(node.arguments, env)
        if len(arguments) == 1 and objs.is_error_object(arguments[0]):
            return arguments[0]
        return apply_function(evaluate, func, arguments)
    else:
        expr_type = type(node)
        assert False, f"unreachable; expression with no known evaluation: {expr_type}\nFound: {node}"


def _evaluate_sequence_of_expressions(arguments: Sequence[Expression], env: Environment) -> list[Object]:
    results: list[Object] = []

    for arg in arguments:
        evaluated = evaluate(arg, env)
        if objs.is_error_object(evaluated):
            return [evaluated]

        results.append(evaluated)

    return results
