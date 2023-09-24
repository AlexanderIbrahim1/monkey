"""
This module contains the FunctionLiteral class, which implements the Expression abstract
class, and represents an `fn`-expression.
"""

from typing import Any

from monkey.parser.statements import BlockStatement
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal

from monkey.parser.expressions.expression import Expression
from monkey.parser.expressions.identifier import Identifier


class FunctionLiteral(Expression):
    def __init__(
        self,
        token: Token,
        parameters: list[Identifier],
        body: BlockStatement,
    ) -> None:
        self._token = token
        self._parameters = parameters
        self._body = body

    def token_literal(self) -> Literal:
        return self._token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FunctionLiteral):
            return NotImplemented

        return (
            (self._token == other._token)
            and (self._parameters == other._parameters)
            and (self._body == other._body)
        )

    def __repr__(self) -> str:
        parameters_list = ", ".join([str(param) for param in self._parameters])

        return f"fn({parameters_list}) {self._body}"
