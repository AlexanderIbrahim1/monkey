"""
This module contains the LetStatement class, a concrete implementation of the Statement
abstract class, for placing `let` statements in the AST.
"""

from monkey.parser.expressions.expression import Expression
from monkey.parser.expressions.identifier import Identifier
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
