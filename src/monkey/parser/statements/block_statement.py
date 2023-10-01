"""
This module contains the BlockStatement class, which implements the Statement
abstract class, and represents a single statement that is composed of several
other Statement instances.
"""

from dataclasses import dataclass
from typing import Any

from monkey.parser.statements.statement import Statement
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal


@dataclass(frozen=True)
class BlockStatement(Statement):
    token: Token
    statements: list[Statement]

    def token_literal(self) -> Literal:
        return self.token.literal

    def statement_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BlockStatement):
            return NotImplemented

        return self.token == other.token and self.statements == other.statements

    def __repr__(self) -> str:
        # if I put multiple statements on different lines, it looks kind of bad without
        # the indentations; but that's something I might worry about later
        # return "{ " + " ".join([f"{stmt}" for stmt in self.statements]) + " }"
        return "\n".join([f"{stmt}" for stmt in self.statements])
