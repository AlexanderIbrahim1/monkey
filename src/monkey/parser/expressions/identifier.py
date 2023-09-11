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
