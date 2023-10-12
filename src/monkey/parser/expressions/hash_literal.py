"""
This module contains the HashLiteral class, which implements the Expression abstract
class, and represents maps of the form

{ <expression> : <expression>, <expression> : <expression>, ... }

"""

from dataclasses import astuple
from dataclasses import dataclass
from typing import Any

from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal

from monkey.parser.expressions.expression import Expression


@dataclass(frozen=True)
class HashLiteral(Expression):
    token: Token  # the '{' token
    key_value_pairs: dict[Expression, Expression]

    def token_literal(self) -> Literal:
        return self.token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, HashLiteral):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        pairs = (f"{key}: {value}" for (key, value) in self.key_value_pairs.items())
        pairs_list = ", ".join([p for p in pairs])

        return f"{{{pairs_list}}}"
