"""
This module contains the IndexExpression class, which implements the Expression abstract
class, and represents expressions of the form
```
    <expression>[<expression>]
```
"""

from dataclasses import astuple
from dataclasses import dataclass
from typing import Any

from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal

from monkey.parser.expressions.expression import Expression


@dataclass(frozen=True)
class IndexExpression(Expression):
    token: Token
    container: Expression
    inside: Expression

    def token_literal(self) -> Literal:
        return self.token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, IndexExpression):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        return f"({self.container}[{self.inside}])"
