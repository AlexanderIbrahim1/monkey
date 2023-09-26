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
