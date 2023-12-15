"""
This module contains the EmptyStatement class, a concrete implementation of the Statement
abstract class, that represents a statement that cannot be meaningfully parsed, but is also
not an error.
"""

from typing import Any

from monkey.parser.statements.statement import Statement
from monkey.tokens.token_types import Literal


EMPTY_STATEMENT_STR = "EMPTY_STATEMENT"


class EmptyStatement(Statement):
    def token_literal(self) -> Literal:
        return EMPTY_STATEMENT_STR

    def statement_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EmptyStatement):
            return NotImplemented

        return True

    def __repr__(self) -> str:
        return EMPTY_STATEMENT_STR
