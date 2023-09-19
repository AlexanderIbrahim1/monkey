import pytest

from monkey.parser.expressions import Expression
from monkey.parser.expressions import InfixExpression
from monkey.parser.expressions import IntegerLiteral
from monkey.tokens import Token
from monkey.tokens import token_types


def test_infix_expression():
    token = Token(token_types.PLUS, "+")
    left = IntegerLiteral(Token(token_types.INT, "5"), "5")
    operator = "+"
    right = IntegerLiteral(Token(token_types.INT, "3"), "3")

    infix = InfixExpression(token, left, operator, right)

    assert str(infix) == "5 + 3"
