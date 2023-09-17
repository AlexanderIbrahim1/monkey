"""
This module contains the ExpressionStatement class, a concrete implementation of the Statement
abstract class, for wrapping around an expression.

For example, in Monkey, we can write
```
x + 10;
```
- in other words, we have a single line consisting of only an expression
"""

from typing import Any

from monkey.parser.expressions import Expression
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal

from monkey.parser.statements.statement import Statement


class ExpressionStatement(Statement):
    def __init__(self, token: Token, value: Expression) -> None:
        self._token = token
        self._value = value

    def token_literal(self) -> Literal:
        return self._token.literal

    def statement_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ExpressionStatement):
            return NotImplemented

        return self._token == other._token and self._value == other._value
