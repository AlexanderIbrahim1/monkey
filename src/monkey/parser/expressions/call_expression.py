"""
This module contains the CallExpression class, which implements the Expression abstract
class, and represents the `(<arguments>)` for calling a function.
"""

from typing import Any

from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal

from monkey.parser.expressions.expression import Expression
from monkey.parser.expressions.identifier import Identifier
from monkey.parser.expressions.function_literal import FunctionLiteral


class CallExpression(Expression):
    def __init__(
        self, token: Token, function: Identifier | FunctionLiteral, arguments: list[Expression]
    ) -> None:
        self._token = token  # '(' token
        self._function = function
        self._arguments = arguments

    def token_literal(self) -> Literal:
        return self._token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CallExpression):
            return NotImplemented

        return (
            (self._token == other._token)
            and (self._function == other._function)
            and (self._arguments == other._arguments)
        )

    def __repr__(self) -> str:
        arguments_list = ", ".join([str(arg) for arg in self._arguments])

        return f"{self._function}({arguments_list})"
