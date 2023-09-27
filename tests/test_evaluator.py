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
