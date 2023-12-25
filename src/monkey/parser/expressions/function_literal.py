"""
This module contains the FunctionLiteral class, which implements the Expression abstract
class, and represents an `fn`-expression.
"""

from dataclasses import dataclass
from typing import Any
from typing import Optional

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
    name: Optional[str] = None

    def token_literal(self) -> Literal:
        return self.token.literal

    def expression_node(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FunctionLiteral):
            return NotImplemented

        # The `astuple()` function would compare the `name` attributes of `self` and `other`
        # using the `==` operator; but they might both be `None`
        #
        # as a result, we can't use it, and the comparisons of each attribute need to be
        # performed explicitly, one-at-a-time
        is_same_token = self.token == other.token
        is_same_parameters = self.parameters == other.parameters
        is_same_body = self.body == other.body

        if self.name is None and other.name is None:
            is_same_name = True
        else:
            is_same_name = self.name == other.name

        return is_same_token and is_same_parameters and is_same_body and is_same_name

    def __repr__(self) -> str:
        if self.name is None:
            name_str = ""
        else:
            name_str = f"{self.name}: "
        parameters_list = ", ".join([str(param) for param in self.parameters])

        return f"{name_str}fn({parameters_list}) {{ {self.body} }}"
