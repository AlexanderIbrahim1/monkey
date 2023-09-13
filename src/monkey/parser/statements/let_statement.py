"""
This module contains the LetStatement class, a concrete implementation of the Statement
abstract class, for placing `let` statements in the AST.
"""

from typing import Any

from monkey.parser.expressions import Expression
from monkey.parser.expressions import Identifier
from monkey.parser.statements.statement import Statement
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal


class LetStatement(Statement):
    def __init__(self, token: Token, name: Identifier, value: Expression) -> None:
        self._token = token
        self._name = name
        self._value = value

    def token_literal(self) -> Literal:
        return self._token.literal

    def statement_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LetStatement):
            return NotImplemented

        return (
            self._token == other._token
            and self._name == other._name
            and self._value == other._value
        )
