"""
This module contains the CallExpression class, which implements the Expression abstract
class, and represents the `(<arguments>)` for calling a function.
"""

from dataclasses import dataclass
from typing import Any
from typing import Sequence

from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal

from monkey.parser.expressions.expression import Expression


@dataclass(frozen=True)
class CallExpression(Expression):
    token: Token  # '(' token
    function: Expression
    arguments: Sequence[Expression]

    def token_literal(self) -> Literal:
        return self.token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CallExpression):
            return NotImplemented

        return (
            (self.token == other.token)
            and (self.function == other.function)
            and (self.arguments == other.arguments)
        )

    def __repr__(self) -> str:
        arguments_list = ", ".join([str(arg) for arg in self.arguments])

        return f"{self.function}({arguments_list})"
