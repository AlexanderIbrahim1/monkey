import pytest

from monkey.lexer import Lexer
from monkey.parser.expressions import BooleanLiteral
from monkey.parser.expressions import Identifier
from monkey.parser.expressions import IfExpression
from monkey.parser.expressions import InfixExpression
from monkey.parser.expressions import IntegerLiteral
from monkey.parser.expressions import PrefixExpression
from monkey.parser.parser import Parser
from monkey.parser.statements import ExpressionStatement
from monkey.parser.statements import BlockStatement
from monkey.parser.statements import LetStatement
from monkey.parser.statements import ReturnStatement
from monkey.tokens import Token
from monkey.tokens import token_types


@pytest.mark.parametrize("monkey_code", ["let x = 5;"])
def test_parse_let_statement(monkey_code):
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    expected_statement = LetStatement(
        Token(token_types.LET, "let"),
        Identifier(Token(token_types.IDENTIFIER, "x"), "x"),
        Identifier(Token(token_types.SEMICOLON, ";"), ";"),
    )

    statement = program[0]

    assert statement == expected_statement
    assert not parser.has_errors()


@pytest.mark.parametrize("monkey_code", ["let = ! 5;"])
def test_failed_parse_let_statement(monkey_code):
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    parser.parse_program()

    assert parser.has_errors()


@pytest.mark.parametrize("monkey_code", ["return 25;"])
def test_parse_return_statement(monkey_code):
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    expected_statement = ReturnStatement(
        Token(token_types.RETURN, "return"),
        Identifier(Token(token_types.SEMICOLON, ";"), ";"),
    )

    statement = program[0]

    assert statement == expected_statement
    assert not parser.has_errors()


def test_identifier_expression():
    monkey_code = "hello;"
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    expected_token = Token(token_types.IDENTIFIER, "hello")
    expected_statement = ExpressionStatement(expected_token, Identifier(expected_token, "hello"))

    assert program.number_of_statements() == 1
    assert program[0] == expected_statement
    assert not parser.has_errors()


def test_integer_literal_expression():
    monkey_code = "5;"
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    expected_token = Token(token_types.INT, "5")
    expected_statement = ExpressionStatement(expected_token, IntegerLiteral(expected_token, "5"))

    assert program.number_of_statements() == 1
    assert program[0] == expected_statement
    assert not parser.has_errors()


@pytest.mark.parametrize(
    "monkey_code, ttype, literal",
    [
        ("!5;", token_types.BANG, "!"),
        ("-5;", token_types.MINUS, "-"),
    ],
)
def test_prefix_expression_integer_literal(monkey_code, ttype, literal):
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    expected_token = Token(ttype, literal)
    expected_integer_expression = IntegerLiteral(Token(token_types.INT, "5"), "5")

    expected_expression = PrefixExpression(expected_token, literal, expected_integer_expression)

    expected_statement = ExpressionStatement(expected_token, expected_expression)

    assert program.number_of_statements() == 1
    assert program[0] == expected_statement
    assert not parser.has_errors()


@pytest.mark.parametrize(
    "monkey_code, prefix_ttype, prefix_literal, boolean_ttype, boolean_literal",
    [
        ("!true;", token_types.BANG, "!", token_types.TRUE, "true"),
        ("!false;", token_types.BANG, "!", token_types.FALSE, "false"),
    ],
)
def test_prefix_expression_boolean_literal(
    monkey_code, prefix_ttype, prefix_literal, boolean_ttype, boolean_literal
):
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    expected_prefix_token = Token(prefix_ttype, prefix_literal)

    expected_boolean_expression = BooleanLiteral(Token(boolean_ttype, boolean_literal), boolean_literal)

    expected_expression = PrefixExpression(expected_prefix_token, prefix_literal, expected_boolean_expression)

    expected_statement = ExpressionStatement(expected_prefix_token, expected_expression)

    assert program.number_of_statements() == 1
    assert program[0] == expected_statement
    assert not parser.has_errors()


@pytest.mark.parametrize(
    "monkey_code, ttype, left, operator, right",
    [
        ("5 + 6;", token_types.PLUS, "5", "+", "6"),
        ("5 - 6;", token_types.MINUS, "5", "-", "6"),
        ("5 * 6;", token_types.ASTERISK, "5", "*", "6"),
        ("5 / 6;", token_types.SLASH, "5", "/", "6"),
        ("5 > 6;", token_types.GT, "5", ">", "6"),
        ("5 < 6;", token_types.LT, "5", "<", "6"),
        ("5 == 6;", token_types.EQ, "5", "==", "6"),
        ("5 != 6;", token_types.NOT_EQ, "5", "!=", "6"),
    ],
)
def test_parsing_infix_expressions(monkey_code, ttype, left, operator, right):
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    expected_token = Token(token_types.INT, left)
    expected_expression = InfixExpression(
        Token(ttype, operator),
        IntegerLiteral(Token(token_types.INT, left), left),
        operator,
        IntegerLiteral(Token(token_types.INT, right), right),
    )

    expected_statement = ExpressionStatement(expected_token, expected_expression)

    assert program.number_of_statements() == 1
    assert program[0] == expected_statement
    assert not parser.has_errors()


@pytest.mark.parametrize(
    "monkey_code, expected",
    [
        ("-a * b;", "((-a) * b)"),
        ("!-a;", "(!(-a))"),
        ("a + b + c;", "((a + b) + c)"),
        ("a + b - c;", "((a + b) - c)"),
        ("a * b * c;", "((a * b) * c)"),
        ("a * b / c;", "((a * b) / c)"),
        ("a + b / c;", "(a + (b / c))"),
        ("a + b * c + d / e - f;", "(((a + (b * c)) + (d / e)) - f)"),
        ("3 + 4; -5 * 5;", "(3 + 4)\n((-5) * 5)"),
        ("5 > 4 == 3 < 4;", "((5 > 4) == (3 < 4))"),
        ("5 < 4 != 3 > 4;", "((5 < 4) != (3 > 4))"),
        ("3 + 4 * 5 == 3 * 1 + 4 * 5;", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),
        ("true;", "true"),
        ("false;", "false"),
        ("3 > 5 == false;", "((3 > 5) == false)"),
        ("3 < 5 == true;", "((3 < 5) == true)"),
        ("1 + (2 + 3) + 4;", "((1 + (2 + 3)) + 4)"),
        ("(5 + 5) * 2;", "((5 + 5) * 2)"),
        ("2 / (5 + 5);", "(2 / (5 + 5))"),
        ("-(5 + 5);", "(-(5 + 5))"),
        ("!(true == true);", "(!(true == true))"),
    ],
)
def test_operator_precedence_parsing(monkey_code, expected):
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    actual = str(program)
    assert actual == expected


@pytest.mark.parametrize(
    "monkey_code, ttype, literal",
    [
        ("true;", token_types.TRUE, "true"),
        ("false;", token_types.FALSE, "false"),
    ],
)
def test_boolean_literal_expression(monkey_code, ttype, literal):
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    expected_token = Token(ttype, literal)
    expected_expression = BooleanLiteral(expected_token, literal)
    expected_statement = ExpressionStatement(expected_token, expected_expression)

    assert program.number_of_statements() == 1
    assert program[0] == expected_statement
    assert not parser.has_errors()


def test_parse_if_expression():
    monkey_code = "if (3 < 5) { 10 } else { 20 };"
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

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

    expected_statement = ExpressionStatement(Token(token_types.IF, "if"), expr)

    assert program.number_of_statements() == 1
    assert program[0] == expected_statement
    assert not parser.has_errors()
