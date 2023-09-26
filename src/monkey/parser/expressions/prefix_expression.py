"""
This module contains the PrefixExpression class, which implements the Expression abstract
class, and represents an expression where there is a prefix operator and an operand.
"""

from dataclasses import dataclass
from typing import Any

from monkey.parser.expressions.expression import Expression
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal


@dataclass(frozen=True)
class PrefixExpression(Expression):
    token: Token
    operator: Literal
    expr: Expression

    def token_literal(self) -> Literal:
        return self.token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PrefixExpression):
            return NotImplemented

        return (self.token == other.token) and (self.operator == other.operator) and (self.expr == other.expr)

    def __repr__(self) -> str:
        return f"({self.operator}{self.expr})"
