"""
This module contains the InfixExpression class, which implements the Expression abstract
class, and represents an expression with a left and right subexpression, and an operator
in the middle of them.
"""

from dataclasses import dataclass
from typing import Any

from monkey.parser.expressions.expression import Expression
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal


@dataclass
class InfixExpression(Expression):
    token: Token
    left: Expression
    operator: Literal
    right: Expression

    def token_literal(self) -> Literal:
        return self.token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, InfixExpression):
            return NotImplemented

        return (
            (self.token == other.token)
            and (self.left == other.left)
            and (self.operator == other.operator)
            and (self.right == other.right)
        )

    def __repr__(self) -> str:
        return f"({self.left} {self.operator} {self.right})"
