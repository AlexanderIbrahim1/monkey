"""
This module contains the FailedExpression class, which implements the Expression abstract
class, and represents an expression that could not be parsed.
"""

from typing import Any

from monkey.parser.expressions.expression import Expression
from monkey.tokens.token_types import Literal


FAILED_EXPRESSION_STR = "FAILED_EXPRESSION"


class FailedExpression(Expression):
    def token_literal(self) -> Literal:
        return FAILED_EXPRESSION_STR

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FailedExpression):
            return NotImplemented

        return True

    def __repr__(self) -> str:
        return FAILED_EXPRESSION_STR
