import pytest

from monkey import Lexer
from monkey import Parser
from monkey.evaluator.evaluator import evaluate
import monkey.object as objs


def test_evaluate_program():
    program = Parser(Lexer("5;")).parse_program()

    assert not program.has_errors()
    assert evaluate(program) == objs.IntegerObject(5)
