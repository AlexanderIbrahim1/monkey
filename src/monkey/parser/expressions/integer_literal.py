"""
This module contains the IntegerLiteral class, which is an Expression that represents
a simple integer literal.
"""

from typing import Any

from monkey.parser.expressions.expression import Expression
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal


class IntegerLiteral(Expression):
    def __init__(self, token: Token, value: Literal) -> None:
        self._token = token
        self._value = value

    def token_literal(self) -> Literal:
        return self._token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, IntegerLiteral):
            return NotImplemented

        return (self._token == other._token) and (self._value == other._value)

    def __repr__(self) -> str:
        return f"{self._value}"
