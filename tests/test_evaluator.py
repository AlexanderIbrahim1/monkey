import pytest

from monkey import Lexer
from monkey import Parser
from monkey.evaluator.evaluator import evaluate
import monkey.object as objs


def test_evaluate_integer_literal():
    program = Parser(Lexer("5;")).parse_program()

    assert not program.has_errors()
    assert evaluate(program) == objs.IntegerObject(5)


@pytest.mark.parametrize(
    "monkey_code, value",
    [
        ("true;", True),
        ("false;", False),
    ],
)
def test_evaluate_boolean_literal(monkey_code, value):
    program = Parser(Lexer(monkey_code)).parse_program()

    assert not program.has_errors()
    assert evaluate(program) == objs.BooleanObject(value)


@pytest.mark.parametrize(
    "monkey_code, expected_value",
    [
        ("!true;", False),
        ("!false;", True),
        ("!5;", False),
        ("!!true;", True),
        ("!!false;", False),
        ("!!123;", True),
    ],
)
def test_bang_operator(monkey_code, expected_value):
    program = Parser(Lexer(monkey_code)).parse_program()

    assert not program.has_errors()
    assert evaluate(program) == objs.BooleanObject(expected_value)


@pytest.mark.parametrize(
    "monkey_code, expected_value",
    [
        ("5;", 5),
        ("-5;", -5),
        ("10;", 10),
        ("-10;", -10),
        ("-0;", 0),
        ("0;", 0),
    ],
)
def test_minus_operator(monkey_code, expected_value):
    program = Parser(Lexer(monkey_code)).parse_program()

    assert not program.has_errors()
    assert evaluate(program) == objs.IntegerObject(expected_value)


@pytest.mark.parametrize(
    "monkey_code, expected_value",
    [
        ("1 + 1;", 2),
        ("2 + 4;", 6),
        ("1 - 1;", 0),
        ("1 - 3;", -2),
        ("-3 + 1;", -2),
        ("2 * 3;", 6),
        ("2 * -3;", -6),
        ("-2 * 3;", -6),
        ("0 * 3;", 0),
        ("6 / 3;", 2),
        ("6 / 2;", 3),
        ("-6 / 2;", -3),
        ("0 / 4;", 0),
    ],
)
def test_integer_algebraic_infix_expression(monkey_code, expected_value):
    program = Parser(Lexer(monkey_code)).parse_program()

    assert not program.has_errors()
    assert evaluate(program) == objs.IntegerObject(expected_value)


@pytest.mark.parametrize(
    "monkey_code, expected_value",
    [
        ("1 == 1;", True),
        ("0 == 0;", True),
        ("2 > 1;", True),
        ("1 < 2;", True),
        ("1 != 2;", True),
        ("2 < 1;", False),
        ("1 > 2;", False),
        ("1 != 1;", False),
    ],
)
def test_integer_logical_infix_expression(monkey_code, expected_value):
    program = Parser(Lexer(monkey_code)).parse_program()

    assert not program.has_errors()
    assert evaluate(program) == objs.BooleanObject(expected_value)
