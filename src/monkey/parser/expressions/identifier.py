"""
This module contains the Identifier class, which implements the Expression abstract
class, and represents an identifier in a statement or another expression.

The decision to make the Identifier class implement the Expression abstract class is
based on both simplicity, and following the book. Obviously, not every identifier is
an expression. For example, in the statement:

    `let x = value;`

`x` is not an expression, but `value` is.

The book chooses to keep all of these lumped under the same class to simplify things.
"""

from typing import Any

from monkey.parser.expressions.expression import Expression
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal


class Identifier(Expression):
    def __init__(self, token: Token, value: Literal) -> None:
        self._token = token
        self._value = value

    def token_literal(self) -> Literal:
        return self._token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Identifier):
            return NotImplemented

        return (self._token == other._token) and (self._value == other._value)

    # TODO: implement this fully later, when the book gets to that part
    def __repr__(self) -> str:
        return "[EXPRESSION STAND-IN]"
