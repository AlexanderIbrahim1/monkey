"""
This module contains the ReturnStatement class, a concrete implementation of the Statement
abstract class, for placing `return` statements in the AST.
"""

from dataclasses import dataclass
from typing import Any

from monkey.parser.expressions.expression import Expression
from monkey.parser.statements.statement import Statement
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal


@dataclass(frozen=True)
class ReturnStatement(Statement):
    token: Token
    value: Expression

    def token_literal(self) -> Literal:
        return self.token.literal

    def statement_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ReturnStatement):
            return NotImplemented

        return self.token == other.token and self.value == other.value

    def __repr__(self) -> str:
        return f"{self.token_literal()} {self.value};"
