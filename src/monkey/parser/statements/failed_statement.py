"""
This module contains the FailedStatement class, a concrete implementation of the Statement
abstract class, that represents a statement that could not be parsed.
"""

from typing import Any

from monkey.parser.statements.statement import Statement
from monkey.tokens.token_types import Literal


FAILED_STATEMENT_STR = "FAILED_STATEMENT"


class FailedStatement(Statement):
    def token_literal(self) -> Literal:
        return FAILED_STATEMENT_STR

    def statement_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FailedStatement):
            return NotImplemented

        return True

    def __repr__(self) -> str:
        return FAILED_STATEMENT_STR
