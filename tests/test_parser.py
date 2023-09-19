import pytest

from monkey.lexer import Lexer
from monkey.parser.expressions import Identifier
from monkey.parser.expressions import IntegerLiteral
from monkey.parser.expressions import PrefixExpression
from monkey.parser.parser import Parser
from monkey.parser.statements import ExpressionStatement
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
    program = parser.parse_program()

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
    expected_statement = ExpressionStatement(
        expected_token, Identifier(expected_token, "hello")
    )

    assert program.number_of_statements() == 1
    assert program[0] == expected_statement
    assert not parser.has_errors()


def test_integer_literal_expression():
    monkey_code = "5;"
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    expected_token = Token(token_types.INT, "5")
    expected_statement = ExpressionStatement(
        expected_token, IntegerLiteral(expected_token, "5")
    )

    assert program.number_of_statements() == 1
    assert program[0] == expected_statement
    assert not parser.has_errors()


def test_prefix_expression_bang():
    monkey_code = "!5;"
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    expected_expression = PrefixExpression(
        Token(token_types.BANG, "!"),
        "!",
        IntegerLiteral(Token(token_types.INT, "5"), "5"),
    )

    expected_token = Token(token_types.BANG, "!")
    expected_statement = ExpressionStatement(expected_token, expected_expression)

    assert program.number_of_statements() == 1
    assert program[0] == expected_statement
    assert not parser.has_errors()


def test_prefix_expression_minus():
    monkey_code = "-5;"
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    expected_expression = PrefixExpression(
        Token(token_types.MINUS, "-"),
        "-",
        IntegerLiteral(Token(token_types.INT, "5"), "5"),
    )

    expected_token = Token(token_types.MINUS, "-")
    expected_statement = ExpressionStatement(expected_token, expected_expression)

    assert program.number_of_statements() == 1
    assert program[0] == expected_statement
    assert not parser.has_errors()


@pytest.mark.parametrize(
    "monkey_code, left, operator, right",
    [
        ("5 + 6;", "5", "+", "6"),
        ("5 - 6;", "5", "-", "6"),
        ("5 * 6;", "5", "*", "6"),
        ("5 / 6;", "5", "/", "6"),
        ("5 > 6;", "5", ">", "6"),
        ("5 < 6;", "5", "<", "6"),
        ("5 == 6;", "5", "==", "6"),
        ("5 != 6;", "5", "!=", "6"),
    ]
)
@pytest.mark.skip
def test_parsing_infix_expressions(monkey_code, left, operator, right):
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    assert program.number_of_statements() == 1
    # TODO: continue writing this test

















