"""
This module contains the Program class, whose instances act as the root node of
every AST that the parser produces.
"""

from typing import Optional

from monkey.parser.ast_node import ASTNode
from monkey.parser.constants import DEFAULT_LITERAL
from monkey.parser.statements import Statement
from monkey.tokens import Literal


class Program(ASTNode):
    def __init__(self, statements: Optional[list[Statement]] = None) -> None:
        if statements is None:
            self._statements: list[Statement] = list()
        else:
            self._statements = statements

    def token_literal(self) -> Literal:
        at_least_one_statement = len(self._statements) > 0

        if at_least_one_statement:
            return self._statements[0].token_literal()
        else:
            return DEFAULT_LITERAL
