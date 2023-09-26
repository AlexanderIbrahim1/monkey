"""
This module contains the evalute function, which is what evaluates the nodes of
the AST that the parser produced.
"""

from monkey.parser import ASTNode
from monkey.parser import Expression
from monkey.parser import Program
from monkey.parser import Statement
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
    result: Object = objs.NullObject()

    for statement in program:
        result = evaluate(statement)

    return result


def _evaluate_statement(node: Statement) -> Object:
    # Each statement is composed of expressions, and thus the role of this function is
    # to recursively call `evaluate()` again for each statement.
    if isinstance(node, stmts.ExpressionStatement):
        return evaluate(node.value)
    else:
        return objs.NullObject()


def _evaluate_expression(node: Expression) -> Object:
    # For an expression, we either create an Object from the expression directly, or we
    # recursively call `evaluate()` to split the expression up into smaller ones
    if isinstance(node, exprs.IntegerLiteral):
        return objs.IntegerObject(int(node.value))
    else:
        return objs.NullObject()
