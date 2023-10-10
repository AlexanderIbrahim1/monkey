import pytest

from monkey import evaluate
import monkey.object as objs

from utils_for_tests import program_and_env


@pytest.mark.parametrize(
    "monkey_code, expected_length",
    [
        ('len("hello");', 5),
        ('len("hello world");', 11),
        ('len("");', 0),
        ("len([1, 2, 3]);", 3),
        ("len([]);", 0),
        ("let x = [1, 2]; len(x);", 2),
    ],
)
def test_len(monkey_code, expected_length):
    program, env = program_and_env(monkey_code)

    assert not program.has_errors()
    assert evaluate(program, env) == objs.IntegerObject(expected_length)


@pytest.mark.parametrize("monkey_code", ["len();", "len([1, 2], [3, 4]);"])
def test_len_invalid_number_of_elements(monkey_code):
    program, env = program_and_env(monkey_code)
    assert not program.has_errors()
    assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)


@pytest.mark.parametrize("monkey_code", ["len(1);", "len(true);"])
def test_len_invalid_argument(monkey_code):
    program, env = program_and_env(monkey_code)
    assert not program.has_errors()
    assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)


@pytest.mark.parametrize(
    "monkey_code, expected_object",
    [
        ('first("hello");', objs.StringObject("h")),
        ('first("hello world");', objs.StringObject("h")),
        ("first([1, 2, 3]);", objs.IntegerObject(1)),
        ("let x = [1, 2]; first(x);", objs.IntegerObject(1)),
    ],
)
def test_first(monkey_code, expected_object):
    program, env = program_and_env(monkey_code)

    assert not program.has_errors()
    assert evaluate(program, env) == expected_object


@pytest.mark.parametrize("monkey_code", ["first();", "first([1, 2], [3, 4]);"])
def test_first_invalid_number_of_elements(monkey_code):
    program, env = program_and_env(monkey_code)
    assert not program.has_errors()
    assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)


@pytest.mark.parametrize("monkey_code", ["first(1);", "first(true);"])
def test_first_invalid_argument(monkey_code):
    program, env = program_and_env(monkey_code)
    assert not program.has_errors()
    assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)


@pytest.mark.parametrize(
    "monkey_code, expected_object",
    [
        ('last("hello");', objs.StringObject("o")),
        ('last("hello world");', objs.StringObject("d")),
        ("last([1, 2, 3]);", objs.IntegerObject(3)),
        ("let x = [1, 2]; last(x);", objs.IntegerObject(2)),
    ],
)
def test_last(monkey_code, expected_object):
    program, env = program_and_env(monkey_code)

    assert not program.has_errors()
    assert evaluate(program, env) == expected_object


@pytest.mark.parametrize("monkey_code", ["last();", "last([1, 2], [3, 4]);"])
def test_last_invalid_number_of_elements(monkey_code):
    program, env = program_and_env(monkey_code)
    assert not program.has_errors()
    assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)


@pytest.mark.parametrize("monkey_code", ["last(1);", "last(true);"])
def test_last_invalid_argument(monkey_code):
    program, env = program_and_env(monkey_code)
    assert not program.has_errors()
    assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)
