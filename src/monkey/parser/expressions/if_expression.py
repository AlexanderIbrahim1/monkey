"""
This module contains the IfExpression class, which implements the Expression abstract
class, and represents both `if` and `if-else` expressions.
"""

from typing import Any

from monkey.parser.expressions.expression import Expression
from monkey.parser.statements import BlockStatement
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal


class IfExpression(Expression):
    def __init__(
        self,
        token: Token,
        condition: Expression,
        consequence: BlockStatement,
        alternative: BlockStatement,
    ) -> None:
        self._token = token
        self._condition = condition
        self._consequence = consequence
        self._alternative = alternative

    def token_literal(self) -> Literal:
        return self._token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, IfExpression):
            return NotImplemented

        return (
            (self._token == other._token)
            and (self._condition == other._condition)
            and (self._consequence == other._consequence)
            and (self._alternative == other._alternative)
        )

    def __repr__(self) -> str:
        if_part = f"if {self._condition} {self._consequence}"

        if (alt_str := str(self._alternative)) != "":
            else_part = f"else {alt_str}"
        else:
            else_part = ""

        return f"{if_part} {else_part}"
