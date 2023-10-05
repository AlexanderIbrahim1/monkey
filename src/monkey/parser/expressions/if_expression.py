"""
This module contains the IfExpression class, which implements the Expression abstract
class, and represents both `if` and `if-else` expressions.
"""

from dataclasses import dataclass
from typing import Any
from typing import Optional

from monkey.parser.expressions.expression import Expression
from monkey.parser.statements import BlockStatement
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal


@dataclass(frozen=True)
class IfExpression(Expression):
    token: Token
    condition: Expression
    consequence: BlockStatement
    alternative: Optional[BlockStatement] = None

    def token_literal(self) -> Literal:
        return self.token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, IfExpression):
            return NotImplemented

        return (
            (self.token == other.token)
            and (self.condition == other.condition)
            and (self.consequence == other.consequence)
            and (self.alternative == other.alternative)
        )

    def __repr__(self) -> str:
        if_part = f"if {self.condition} {{ {self.consequence} }}"
        else_part = f"else {{ {self.alternative} }}" if self.alternative is not None else ""

        return f"{if_part} {else_part}"
