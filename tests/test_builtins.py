import pytest


from monkey import evaluate
from monkey import Lexer
from monkey import Parser
from monkey import parse_program
from monkey import Environment

import monkey.object as objs


@pytest.mark.parametrize(
    "monkey_code, expected_length",
    [
        ('len("hello");', 5),
        ('len("hello world");', 11),
        ('len("");', 0),
    ],
)
def test_len(monkey_code, expected_length):
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parse_program(parser)
    env = Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.IntegerObject(expected_length)
