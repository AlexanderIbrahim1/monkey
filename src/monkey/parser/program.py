"""
This module contains the Program class, whose instances act as the root node of
every AST that the parser produces.
"""

from typing import Any
from typing import Iterator
from typing import Sequence

from monkey.parser.ast_node import ASTNode
from monkey.parser.constants import DEFAULT_LITERAL
from monkey.parser.statements import Statement
from monkey.tokens import Literal


class Program(ASTNode):
    def __init__(self) -> None:
        self._statements: list[Statement] = list()
        self._errors: list[str] = list()

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def errors(self) -> list[str]:
        return self._errors

    def add_error(self, error: str | Sequence[str]) -> None:
        if isinstance(error, str):
            self._errors.append(error)
        else:
            self._errors.extend(error)

    def number_of_statements(self) -> int:
        return len(self._statements)

    def token_literal(self) -> Literal:
        at_least_one_statement = len(self._statements) > 0

        if at_least_one_statement:
            return self._statements[0].token_literal()
        else:
            return DEFAULT_LITERAL

    def append(self, statement: Statement) -> None:
        self._statements.append(statement)

    def __getitem__(self, index: int) -> Statement:
        return self._statements[index]

    def __repr__(self) -> str:
        return "\n".join([str(s) for s in self._statements])

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Program):
            return NotImplemented

        return self._statements == other._statements

    def __iter__(self) -> Iterator:
        return iter(self._statements)
