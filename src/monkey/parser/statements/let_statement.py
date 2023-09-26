"""
This module contains the LetStatement class, a concrete implementation of the Statement
abstract class, for placing `let` statements in the AST.
"""

from dataclasses import dataclass
from typing import Any

from monkey.parser.expressions import Expression
from monkey.parser.expressions import Identifier
from monkey.parser.statements.statement import Statement
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal


@dataclass(frozen=True)
class LetStatement(Statement):
    token: Token
    name: Identifier
    value: Expression

    def token_literal(self) -> Literal:
        return self.token.literal

    def statement_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LetStatement):
            return NotImplemented

        return self.token == other.token and self.name == other.name and self.value == other.value

    def __repr__(self) -> str:
        return f"{self.token_literal()} {self.name} = {self.value};"
