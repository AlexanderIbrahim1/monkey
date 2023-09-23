import pytest

from monkey.parser.expressions import Expression
from monkey.parser.expressions import IfExpression
from monkey.parser.expressions import InfixExpression
from monkey.parser.expressions import IntegerLiteral
from monkey.parser.statements import BlockStatement
from monkey.parser.statements import ExpressionStatement
from monkey.tokens import Token
from monkey.tokens import token_types


def test_infix_expression():
    token = Token(token_types.PLUS, "+")
    left = IntegerLiteral(Token(token_types.INT, "5"), "5")
    operator = "+"
    right = IntegerLiteral(Token(token_types.INT, "3"), "3")

    infix = InfixExpression(token, left, operator, right)

    assert str(infix) == "(5 + 3)"


def test_if_expression():
    token = Token(token_types.IF, "if")

    condition = InfixExpression(
        Token(token_types.LT, "<"),
        IntegerLiteral(Token(token_types.INT, "3"), "3"),
        token_types.LT,
        IntegerLiteral(Token(token_types.INT, "5"), "5"),
    )

    consequence = BlockStatement(
        Token(token_types.LBRACE, "{"),
        [
            ExpressionStatement(
                Token(token_types.INT, "10"),
                IntegerLiteral(Token(token_types.INT, "10"), "10"),
            )
        ],
    )

    alternative = BlockStatement(
        Token(token_types.LBRACE, "{"),
        [
            ExpressionStatement(
                Token(token_types.INT, "20"),
                IntegerLiteral(Token(token_types.INT, "20"), "20"),
            )
        ],
    )

    expr = IfExpression(token, condition, consequence, alternative)

    assert str(expr) == "if (3 < 5) { 10 } else { 20 }"
