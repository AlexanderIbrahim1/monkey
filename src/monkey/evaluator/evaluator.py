"""
This module contains the evalute function, which is what evaluates the nodes of
the AST that the parser produced.
"""

from typing import Optional

from monkey.parser import ASTNode
from monkey.parser import Expression
from monkey.parser import Program
from monkey.parser import Statement
import monkey.parser.expressions as exprs
import monkey.parser.statements as stmts

from monkey.object import Object
from monkey.object import NullObject


def evaluate(node: ASTNode) -> Optional[Object]:
    if isinstance(node, Program):
        return _evaluate_program_statements(node)
    elif isinstance(node, stmts.ExpressionStatement):
        # TODO: continue


def _evaluate_program_statements(program: Program) -> Object:
    result = NullObject()

    for statement in program:
        result = evaluate(statement)

    return result
    
