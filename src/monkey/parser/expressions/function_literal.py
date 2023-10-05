"""
This module contains the FunctionLiteral class, which implements the Expression abstract
class, and represents an `fn`-expression.
"""

from dataclasses import dataclass
from typing import Any

from monkey.parser.statements import BlockStatement
from monkey.tokens.monkey_token import Token
from monkey.tokens.token_types import Literal

from monkey.parser.expressions.expression import Expression
from monkey.parser.expressions.identifier import Identifier


@dataclass(frozen=True)
class FunctionLiteral(Expression):
    token: Token
    parameters: list[Identifier]
    body: BlockStatement

    def token_literal(self) -> Literal:
        return self.token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FunctionLiteral):
            return NotImplemented

        return (
            (self.token == other.token)
            and (self.parameters == other.parameters)
            and (self.body == other.body)
        )

    def __repr__(self) -> str:
        parameters_list = ", ".join([str(param) for param in self.parameters])

        return f"fn({parameters_list}) {{ {self.body} }}"
