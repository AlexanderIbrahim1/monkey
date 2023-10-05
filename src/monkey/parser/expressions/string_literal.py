"""
This module contains the StringLiteral class, which is an Expression that represents
a simple string literal.
"""

from dataclasses import astuple
from dataclasses import dataclass
from typing import Any

from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal

from monkey.parser.expressions.expression import Expression


@dataclass(frozen=True)
class StringLiteral(Expression):
    token: Token
    value: Literal

    def token_literal(self) -> Literal:
        return self.token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, StringLiteral):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        return f'"{self.value}"'
