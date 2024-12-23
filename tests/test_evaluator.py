import pytest

from monkey import Lexer
from monkey import Parser
from monkey.parser.parser import parse_program
from monkey.evaluator.evaluator import evaluate
from monkey.tokens import token_types
import monkey.object as objs

from utils_for_tests import program_and_env


def test_evaluate_integer_literal():
    program = parse_program(Parser(Lexer("5;")))
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.IntegerObject(5)


@pytest.mark.parametrize(
    "monkey_code, value",
    [
        ("true;", True),
        ("false;", False),
    ],
)
def test_evaluate_boolean_literal(monkey_code, value):
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.BooleanObject(value)


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
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.BooleanObject(expected_value)


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
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.IntegerObject(expected_value)


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
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.IntegerObject(expected_value)


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
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.BooleanObject(expected_value)


@pytest.mark.parametrize(
    "monkey_code, expected_value",
    [
        ("true == true;", True),
        ("false == false ;", True),
        ("true != false;", True),
        ("false != true;", True),
        ("true != true;", False),
        ("false != false ;", False),
        ("true == false;", False),
        ("false == true;", False),
    ],
)
def test_boolean_infix_expression(monkey_code, expected_value):
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.BooleanObject(expected_value)


@pytest.mark.parametrize(
    "monkey_code, expected_value, object_type",
    [
        ("if (true) { 10 };", 10, objs.IntegerObject),
        ("if (1) { 10 };", 10, objs.IntegerObject),
        ("if (1 < 2) { 10 };", 10, objs.IntegerObject),
        ("if (1 > 2) { 10 } else { 20 };", 20, objs.IntegerObject),
        ("if (1 < 2) { 10 } else { 20 };", 10, objs.IntegerObject),
    ],
)
def test_if_else_expression(monkey_code, expected_value, object_type):
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == object_type(expected_value)


@pytest.mark.parametrize(
    "monkey_code",
    [
        "if (false) { 10 };",
        "if (1 > 2) { 20 };",
        "if (2 < 1) { 30 };",
        "if (3 != 3) { 40 };",
    ],
)
def test_if_else_expression_for_null(monkey_code):
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.NULL_OBJ


@pytest.mark.parametrize(
    "monkey_code, expected_value",
    [
        ("return 10;", 10),
        ("return 10; 7;", 10),
        ("7; return 10;", 10),
        ("7; return 10; 123;", 10),
    ],
)
def test_return_statement(monkey_code, expected_value):
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.IntegerObject(expected_value)


@pytest.mark.parametrize(
    "monkey_code, expected_value",
    [
        ("if (3 > 2) { return 10; };", 10),
        ("if (3 > 2) { return 10; } else { return 20; };", 10),
        ("if (2 > 3) { return 10; } else { return 20; };", 20),
    ],
)
def test_return_in_if_statement(monkey_code, expected_value):
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.IntegerObject(expected_value)


def test_return_in_nested_if_statement():
    monkey_code = """
    if (10 > 1) {
        if (10 > 1) {
            return 123;
        }
        return 456;
    };
    """
    expected_value = 123

    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.IntegerObject(expected_value)


@pytest.mark.parametrize(
    "monkey_code, left_type, right_type, operator",
    [
        ("true + 10;", objs.ObjectType.BOOLEAN, objs.ObjectType.INTEGER, token_types.PLUS),
        ("if (10 > 1) { true + 10 };", objs.ObjectType.BOOLEAN, objs.ObjectType.INTEGER, token_types.PLUS),
        ("true + 10; 5;", objs.ObjectType.BOOLEAN, objs.ObjectType.INTEGER, token_types.PLUS),
        ("10 + false;", objs.ObjectType.INTEGER, objs.ObjectType.BOOLEAN, token_types.PLUS),
        ("true - 10;", objs.ObjectType.BOOLEAN, objs.ObjectType.INTEGER, token_types.MINUS),
        ("10 - false;", objs.ObjectType.INTEGER, objs.ObjectType.BOOLEAN, token_types.MINUS),
        ('"hello" + 10;', objs.ObjectType.STRING, objs.ObjectType.INTEGER, token_types.PLUS),
        ('"hello" + true;', objs.ObjectType.STRING, objs.ObjectType.BOOLEAN, token_types.PLUS),
    ],
)
def test_type_mismatch_error(monkey_code, left_type, right_type, operator):
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    err_output = evaluate(program, env)
    assert err_output == objs.TypeMismatchErrorObject(left_type, right_type, operator)


@pytest.mark.parametrize(
    "monkey_code, left_type, right_type, operator",
    [
        ("true / true;", objs.ObjectType.BOOLEAN, objs.ObjectType.BOOLEAN, token_types.SLASH),
        ("true / true; return 123;", objs.ObjectType.BOOLEAN, objs.ObjectType.BOOLEAN, token_types.SLASH),
        ("true + true;", objs.ObjectType.BOOLEAN, objs.ObjectType.BOOLEAN, token_types.PLUS),
        ("true - false;", objs.ObjectType.BOOLEAN, objs.ObjectType.BOOLEAN, token_types.MINUS),
        ("false * false;", objs.ObjectType.BOOLEAN, objs.ObjectType.BOOLEAN, token_types.ASTERISK),
        ('"hello" * "world";', objs.ObjectType.STRING, objs.ObjectType.STRING, token_types.ASTERISK),
        ('"hello" - "world";', objs.ObjectType.STRING, objs.ObjectType.STRING, token_types.MINUS),
        ('"hello" / "world";', objs.ObjectType.STRING, objs.ObjectType.STRING, token_types.SLASH),
    ],
)
def test_unknown_infix_operator_error(monkey_code, left_type, right_type, operator):
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    err_output = evaluate(program, env)
    assert err_output == objs.UnknownInfixOperatorErrorObject(left_type, right_type, operator)


@pytest.mark.parametrize(
    "monkey_code, left_type, operator",
    [
        ("-true;", objs.ObjectType.BOOLEAN, token_types.MINUS),
    ],
)
def test_unknown_prefix_operator_error(monkey_code, left_type, operator):
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    err_output = evaluate(program, env)
    assert err_output == objs.UnknownPrefixOperatorErrorObject(left_type, operator)


@pytest.mark.parametrize("monkey_code, identifier_name", [("a;", "a"), ("a + b;", "a")])
def test_unknown_identifier_operator_error(monkey_code, identifier_name):
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    err_output = evaluate(program, env)
    assert err_output == objs.UnknownIdentifierErrorObject(identifier_name)


@pytest.mark.parametrize(
    "monkey_code, expected_value",
    [
        ("let identity = fn(x) { x }; identity(5);", 5),
        ("let identity = fn(x) { return x; }; identity(5);", 5),
        ("let double = fn(x) { return 2 * x; }; double(5);", 10),
        ("let add = fn(x, y) { x + y }; add(5, 3);", 8),
        ("let add = fn(x, y) { x + y }; add(5, add(2, 1));", 8),
        ("fn(x) { x }(5);", 5),
    ],
)
def test_function_application_on_integers(monkey_code, expected_value):
    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    assert evaluate(program, env) == objs.IntegerObject(expected_value)


# NOTE:
# - this is why we create a new environment for the function, that encloses the surrounding
#   environment; it allows us to contain variables from the surroundings, and the current function
# - this means we get closures for free!
# - it also saves us the trouble of having to get rid of the function's local variables from the
#   surrounding environment (if we had extended the surrounding environment instead)
def test_closure():
    monkey_code = """
        let new_adder = fn(x) {
            let new_func = fn(y) {
                return x + y;
            };

            return new_func;
        };

        let add_two = new_adder(2);
        add_two(2);
    """
    expected_value = 4

    program = parse_program(Parser(Lexer(monkey_code)))
    env = objs.Environment()

    assert evaluate(program, env) == objs.IntegerObject(expected_value)


def test_evaluate_string_literal():
    monkey_code = '"hello world";'
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parse_program(parser)
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.StringObject("hello world")


@pytest.mark.parametrize(
    "monkey_code, expected_value",
    [
        ('"hello" + " world";', "hello world"),
    ],
)
def test_string_concatenation(monkey_code, expected_value):
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parse_program(parser)
    env = objs.Environment()

    assert not program.has_errors()
    assert evaluate(program, env) == objs.StringObject("hello world")


def test_evaluate_array_literal():
    monkey_code = '[1, 2 * 2, 3 - 4, true, "hello" + " world"];'
    program, env = program_and_env(monkey_code)

    expected_object = objs.ArrayObject(
        [
            objs.IntegerObject(1),
            objs.IntegerObject(4),
            objs.IntegerObject(-1),
            objs.BooleanObject(True),
            objs.StringObject("hello world"),
        ]
    )

    assert not program.has_errors()
    assert evaluate(program, env) == expected_object


@pytest.mark.parametrize(
    "monkey_code, expected_value",
    [
        ("[1, 2, 3][0];", 1),
        ("[1, 2, 3][1];", 2),
        ("[1, 2, 3][2];", 3),
        ("let i = 0; [1][i];", 1),
        ("[1, 2, 3][1 + 1];", 3),
        ("let my_array = [1, 2, 3]; my_array[0];", 1),
        ("let my_array = [1, 2, 3]; my_array[0] + my_array[1];", 3),
        ("let my_array = [1, 2, 3]; let i = my_array[0]; my_array[i];", 2),
    ],
)
def test_array_index_expression_with_integers(monkey_code, expected_value):
    program, env = program_and_env(monkey_code)

    assert not program.has_errors()
    assert evaluate(program, env) == objs.IntegerObject(expected_value)


@pytest.mark.parametrize(
    "monkey_code, index, size",
    [
        ("[][3];", 3, 0),
        ("[1, 2, 3][3];", 3, 3),
        ("[1, 2, 3][5];", 5, 3),
        ("[1, 2, 3][-1];", -1, 3),
    ],
)
def test_out_of_bounds_array_index_expression(monkey_code, index, size):
    program, env = program_and_env(monkey_code)

    expected_error = objs.OutOfBoundsErrorObject(objs.ObjectType.ARRAY, index, size)

    assert not program.has_errors()
    assert evaluate(program, env) == expected_error


@pytest.mark.parametrize(
    "monkey_code, expected_value",
    [
        ('"hello"[0];', "h"),
        ('"hello"[1];', "e"),
        ('"hello"[4];', "o"),
        ('"hello world"[5];', " "),
        ('"hello world"[6];', "w"),
    ],
)
def test_string_index_expression(monkey_code, expected_value):
    program, env = program_and_env(monkey_code)

    assert not program.has_errors()
    assert evaluate(program, env) == objs.StringObject(expected_value)


def test_evaluate_hash_literal_1():
    monkey_code = '{"one": 1};'
    program, env = program_and_env(monkey_code)

    key0 = objs.StringObject("one")
    value0 = objs.IntegerObject(1)
    object_hash0 = objs.create_object_hash(key0)
    kv_pair0 = objs.HashKeyValuePair(key0, value0)

    pairs = {object_hash0: kv_pair0}
    expected_hash_object = objs.HashObject(pairs)

    assert not program.has_errors()
    assert evaluate(program, env) == expected_hash_object


def test_evaluate_hash_literal_2():
    # fmt: off
    monkey_code = """{
        "zero": 0,
        "one": 1,
        "two": 1 + 1,
        "thr" + "ee": 6 / 2,
        4: 4,
        true: 5,
        false: 6
    };"""
    # fmt: on
    program, env = program_and_env(monkey_code)

    key0 = objs.StringObject("zero")
    object_hash0 = objs.create_object_hash(key0)
    kv_pair0 = objs.HashKeyValuePair(key0, objs.IntegerObject(0))

    key1 = objs.StringObject("one")
    object_hash1 = objs.create_object_hash(key1)
    kv_pair1 = objs.HashKeyValuePair(key1, objs.IntegerObject(1))

    key2 = objs.StringObject("two")
    object_hash2 = objs.create_object_hash(key2)
    kv_pair2 = objs.HashKeyValuePair(key2, objs.IntegerObject(2))

    key3 = objs.StringObject("three")
    object_hash3 = objs.create_object_hash(key3)
    kv_pair3 = objs.HashKeyValuePair(key3, objs.IntegerObject(3))

    key4 = objs.IntegerObject(4)
    object_hash4 = objs.create_object_hash(key4)
    kv_pair4 = objs.HashKeyValuePair(key4, objs.IntegerObject(4))

    key5 = objs.BooleanObject(True)
    object_hash5 = objs.create_object_hash(key5)
    kv_pair5 = objs.HashKeyValuePair(key5, objs.IntegerObject(5))

    key6 = objs.BooleanObject(False)
    object_hash6 = objs.create_object_hash(key6)
    kv_pair6 = objs.HashKeyValuePair(key6, objs.IntegerObject(6))

    pairs = dict(
        [
            (object_hash0, kv_pair0),
            (object_hash1, kv_pair1),
            (object_hash2, kv_pair2),
            (object_hash3, kv_pair3),
            (object_hash4, kv_pair4),
            (object_hash5, kv_pair5),
            (object_hash6, kv_pair6),
        ]
    )
    expected_hash_object = objs.HashObject(pairs)

    assert not program.has_errors()
    assert evaluate(program, env) == expected_hash_object


@pytest.mark.parametrize(
    "monkey_code, expected_value",
    [
        ('{"one": 1}["one"];', 1),
        ('{"one": 1, "two": 2}["one"];', 1),
        ('{"two": 2, "one": 1}["one"];', 1),
        ('let x = {"one": 1}; x["one"];', 1),
        ('let x = {"three": 2 + 1}; x["three"];', 3),
        ("let x = {2 + 1: 3}; x[3];", 3),
        ("{true: 1}[true];", 1),
        ("{false: 1}[false];", 1),
    ],
)
def test_hash_index_expression(monkey_code, expected_value):
    program, env = program_and_env(monkey_code)

    assert not program.has_errors()
    assert evaluate(program, env) == objs.IntegerObject(expected_value)


@pytest.mark.parametrize(
    "monkey_code, key",
    [
        ('{"one": 1}["two"];', objs.StringObject("two")),
        ('{}["two"];', objs.StringObject("two")),
    ],
)
def test_key_not_found_hash_index_expression(monkey_code, key):
    program, env = program_and_env(monkey_code)

    expected_error = objs.KeyNotFoundErrorObject(key)

    assert not program.has_errors()
    assert evaluate(program, env) == expected_error
