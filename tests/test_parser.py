import pytest

from monkey.lexer import Lexer
from monkey.parser.expressions import Identifier
from monkey.parser.parser import Parser
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

