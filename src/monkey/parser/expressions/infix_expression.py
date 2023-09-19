"""
This module contains the InfixExpression class, which implements the Expression abstract
class, and represents an expression with a left and right subexpression, and an operator
in the middle of them.
"""

from typing import Any

from monkey.parser.expressions.expression import Expression
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal


class InfixExpression(Expression):
    def __init__(
        self, token: Token, left: Expression, operator: Literal, right: Expression
    ) -> None:
        self._token = token
        self._left = left
        self._operator = operator
        self._right = right

    def token_literal(self) -> Literal:
        return self._token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, InfixExpression):
            return NotImplemented

        return (
            (self._token == other._token)
            and (self._left == other._left)
            and (self._operator == other._operator)
            and (self._right == other._right)
        )

    def __repr__(self) -> str:
        return f"{self._left} {self._operator} {self._right}"
