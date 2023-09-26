"""
This module contains the BooleanLiteral class, which is an Expression that represents
a simple boolean literal.
"""

from dataclasses import dataclass
from typing import Any

from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal

from monkey.parser.expressions.expression import Expression


@dataclass(frozen=True)
class BooleanLiteral(Expression):
    token: Token
    value: Literal

    def token_literal(self) -> Literal:
        return self.token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BooleanLiteral):
            return NotImplemented

        return (self.token == other.token) and (self.value == other.value)

    def __repr__(self) -> str:
        return f"{self.value}"
