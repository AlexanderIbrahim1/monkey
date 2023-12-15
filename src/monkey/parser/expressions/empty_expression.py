"""
This module contains the EmptyExpression class, which implements the Expression abstract
class, and represents an expression that cannot be meaningfully parsed, but is also not
an error.
"""

from typing import Any

from monkey.parser.expressions.expression import Expression
from monkey.tokens.token_types import Literal


EMPTY_EXPRESSION_STR = "EMPTY_EXPRESSION"


class EmptyExpression(Expression):
    def token_literal(self) -> Literal:
        return EMPTY_EXPRESSION_STR

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EmptyExpression):
            return NotImplemented

        return True

    def __repr__(self) -> str:
        return EMPTY_EXPRESSION_STR
