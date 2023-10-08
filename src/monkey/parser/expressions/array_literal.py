"""
This module contains the ArrayLiteral class, which implements the Expression abstract
class, and represents bracket-surrounded, comma-separated sequences of other expressions.
"""

from dataclasses import astuple
from dataclasses import dataclass
from typing import Any

from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal

from monkey.parser.expressions.expression import Expression


@dataclass
class ArrayLiteral(Expression):
    token: Token
    elements: list[Expression]

    def token_literal(self) -> Literal:
        return self.token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ArrayLiteral):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        elements_str = ", ".join([str(elem) for elem in self.elements])
        return f"[{elements_str}]"
