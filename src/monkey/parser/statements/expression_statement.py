"""
This module contains the ExpressionStatement class, a concrete implementation of the Statement
abstract class, for wrapping around an expression.

For example, in Monkey, we can write
```
x + 10;
```
- in other words, we have a single line consisting of only an expression
"""

from dataclasses import dataclass
from typing import Any

from monkey.parser.expressions import Expression
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal

from monkey.parser.statements.statement import Statement


@dataclass(frozen=True)
class ExpressionStatement(Statement):
    token: Token
    value: Expression

    def token_literal(self) -> Literal:
        return self.token.literal

    def statement_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ExpressionStatement):
            return NotImplemented

        return self.token == other.token and self.value == other.value

    def __repr__(self) -> str:
        return f"{self.value}"
