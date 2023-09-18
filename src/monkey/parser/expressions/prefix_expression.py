"""
This module contains the PrefixExpression class, which implements the Expression abstract
class, and represents an expression where there is a prefix operator and an operand.
"""

from typing import Any

from monkey.parser.expressions.expression import Expression
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal


class PrefixExpression(Expression):
    def __init__(self, token: Token, operator: Literal, expr: Expression) -> None:
        self._token = token
        self._operator = operator
        self._expr = expr

    def token_literal(self) -> Literal:
        return self._token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PrefixExpression):
            return NotImplemented

        return (
            (self._token == other._token)
            and (self._operator == other._operator)
            and (self._expr == other._expr)
        )

    def __repr__(self) -> str:
        return f"({self._operator}{self._expr})"
