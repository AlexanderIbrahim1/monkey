from typing import Sequence

import pytest

from monkey import evaluate
import monkey.object as objs

from utils_for_tests import program_and_env


class TestBuiltin_len:
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
    def test_len(self, monkey_code, expected_length):
        program, env = program_and_env(monkey_code)

        assert not program.has_errors()
        assert evaluate(program, env) == objs.IntegerObject(expected_length)

    @pytest.mark.parametrize("monkey_code", ["len();", "len([1, 2], [3, 4]);"])
    def test_len_invalid_number_of_elements(self, monkey_code):
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)

    @pytest.mark.parametrize("monkey_code", ["len(1);", "len(true);"])
    def test_len_invalid_argument(self, monkey_code):
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)


class TestBuiltin_first:
    @pytest.mark.parametrize(
        "monkey_code, expected_object",
        [
            ('first("hello");', objs.StringObject("h")),
            ('first("hello world");', objs.StringObject("h")),
            ("first([1, 2, 3]);", objs.IntegerObject(1)),
            ("let x = [1, 2]; first(x);", objs.IntegerObject(1)),
        ],
    )
    def test_first(self, monkey_code, expected_object):
        program, env = program_and_env(monkey_code)

        assert not program.has_errors()
        assert evaluate(program, env) == expected_object

    @pytest.mark.parametrize("monkey_code", ["first();", "first([1, 2], [3, 4]);"])
    def test_first_invalid_number_of_elements(self, monkey_code):
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)

    @pytest.mark.parametrize("monkey_code", ["first(1);", "first(true);"])
    def test_first_invalid_argument(self, monkey_code):
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)


class TestBuiltin_last:
    @pytest.mark.parametrize(
        "monkey_code, expected_object",
        [
            ('last("hello");', objs.StringObject("o")),
            ('last("hello world");', objs.StringObject("d")),
            ("last([1, 2, 3]);", objs.IntegerObject(3)),
            ("let x = [1, 2]; last(x);", objs.IntegerObject(2)),
        ],
    )
    def test_last(self, monkey_code, expected_object):
        program, env = program_and_env(monkey_code)

        assert not program.has_errors()
        assert evaluate(program, env) == expected_object

    @pytest.mark.parametrize("monkey_code", ["last();", "last([1, 2], [3, 4]);"])
    def test_last_invalid_number_of_elements(self, monkey_code):
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)

    @pytest.mark.parametrize("monkey_code", ["last(1);", "last(true);"])
    def test_last_invalid_argument(self, monkey_code):
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)


class TestBuiltin_rest:
    @pytest.mark.parametrize(
        "monkey_code, expected_object",
        [
            ('rest("hello");', objs.StringObject("ello")),
            ('rest("hello world");', objs.StringObject("ello world")),
            ("rest([1, 2, 3]);", objs.ArrayObject([objs.IntegerObject(2), objs.IntegerObject(3)])),
            ("let x = [1, 2]; rest(x);", objs.ArrayObject([objs.IntegerObject(2)])),
            ("let x = [10]; rest(x);", objs.ArrayObject([])),
        ],
    )
    def test_rest(self, monkey_code, expected_object):
        program, env = program_and_env(monkey_code)

        assert not program.has_errors()
        assert evaluate(program, env) == expected_object

    @pytest.mark.parametrize("monkey_code", ["rest();", "rest([1, 2], [3, 4]);"])
    def test_rest_invalid_number_of_elements(self, monkey_code):
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)

    @pytest.mark.parametrize("monkey_code", ["rest(1);", "rest(true);"])
    def test_rest_invalid_argument(self, monkey_code):
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)


def make_integer_array(integers: Sequence[int]) -> objs.ArrayObject:
    return objs.ArrayObject([objs.IntegerObject(i) for i in integers])


class TestBuiltin_push:
    @pytest.mark.parametrize(
        "monkey_code, expected_object",
        [
            ('push("hello", "x");', objs.StringObject("hellox")),
            ('push("hello world", "!");', objs.StringObject("hello world!")),
            ("push([1, 2], 3);", make_integer_array([1, 2, 3])),
            ("let x = [1, 2]; push(x, 3);", make_integer_array([1, 2, 3])),
            ("let x = []; push(x, 1);", make_integer_array([1])),
        ],
    )
    def test_push(self, monkey_code, expected_object):
        program, env = program_and_env(monkey_code)

        assert not program.has_errors()
        assert evaluate(program, env) == expected_object

    @pytest.mark.parametrize("monkey_code", ["push();", "push([1, 2]);", "push([1], 2, 3);"])
    def test_push_invalid_number_of_elements(self, monkey_code):
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)

    @pytest.mark.parametrize("monkey_code", ["push(1, 1);", "push(true, false);"])
    def test_push_invalid_argument(self, monkey_code):
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)

    def test_push_invalid_string(self):
        monkey_code = 'push("hello", "wow");'
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)


class TestBuiltin_pop:
    @pytest.mark.parametrize(
        "monkey_code, expected_object",
        [
            ('pop("hello");', objs.StringObject("hell")),
            ('pop("hello world");', objs.StringObject("hello worl")),
            ("pop([1, 2]);", make_integer_array([1])),
            ("let x = [1, 2]; pop(x);", make_integer_array([1])),
            ("let x = [1]; pop(x);", make_integer_array([])),
        ],
    )
    def test_pop(self, monkey_code, expected_object):
        program, env = program_and_env(monkey_code)

        assert not program.has_errors()
        assert evaluate(program, env) == expected_object

    @pytest.mark.parametrize("monkey_code", ["pop();", "pop([1], [2]);"])
    def test_pop_invalid_number_of_elements(self, monkey_code):
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)

    @pytest.mark.parametrize("monkey_code", ["pop(1);", "pop(true);"])
    def test_pop_invalid_argument(self, monkey_code):
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)

    @pytest.mark.parametrize("monkey_code", ["pop([]);", "pop(" ");"])
    def test_pop_empty_container(self, monkey_code):
        program, env = program_and_env(monkey_code)
        assert not program.has_errors()
        assert isinstance(evaluate(program, env), objs.BuiltinErrorObject)
