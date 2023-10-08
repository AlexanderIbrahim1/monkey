from monkey.parser.expressions import ArrayLiteral
from monkey.parser.expressions import BooleanLiteral
from monkey.parser.expressions import FunctionLiteral
from monkey.parser.expressions import Identifier
from monkey.parser.expressions import IfExpression
from monkey.parser.expressions import InfixExpression
from monkey.parser.expressions import IntegerLiteral
from monkey.parser.statements import BlockStatement
from monkey.parser.statements import ExpressionStatement
from monkey.parser.statements import ReturnStatement
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


def test_function_literal():
    token = Token(token_types.FUNCTION, "fn")

    parameters = [
        Identifier(Token(token_types.IDENTIFIER, "x"), "x"),
        Identifier(Token(token_types.IDENTIFIER, "y"), "y"),
    ]

    summation = InfixExpression(
        Token(token_types.PLUS, "+"),
        Identifier(Token(token_types.IDENTIFIER, "x"), "x"),
        token_types.PLUS,
        Identifier(Token(token_types.IDENTIFIER, "y"), "y"),
    )

    ret_statement = ReturnStatement(Token(token_types.RETURN, "return"), summation)
    body = BlockStatement(Token(token_types.LBRACE, "{"), [ret_statement])

    expr = FunctionLiteral(token, parameters, body)

    assert str(expr) == "fn(x, y) { return (x + y); }"


def test_array_literal():
    token = Token(token_types.LBRACKET, "[")

    elements = [
        Identifier(Token(token_types.IDENTIFIER, "x"), "x"),
        Identifier(Token(token_types.IDENTIFIER, "y"), "y"),
        IntegerLiteral(Token(token_types.INT, "20"), "20"),
        BooleanLiteral(Token(token_types.TRUE, "true"), "true"),
    ]

    expr = ArrayLiteral(token, elements)
    assert str(expr) == "[x, y, 20, true]"


def test_array_literal_empty():
    token = Token(token_types.LBRACKET, "[")
    expr = ArrayLiteral(token, [])
    assert str(expr) == "[]"
