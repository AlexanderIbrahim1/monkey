import pytest

from monkey.tokens import Token
from monkey.tokens import token_types

from monkey.object import ObjectType
from monkey.object import IntegerObject
from monkey.object import BooleanObject
from monkey.object import NullObject
from monkey.object import ReturnObject
from monkey.object import FunctionObject
from monkey.object import ArrayObject
from monkey.object import CompiledFunctionObject

from monkey.parser.expressions import Identifier
from monkey.parser.expressions import InfixExpression
from monkey.parser.statements import BlockStatement
from monkey.parser.statements import ReturnStatement
import monkey.object as objs

from monkey.code import make_instruction
from monkey.code import instructions_to_string
from monkey.code import opcodes


def test_integer_object():
    int_obj = IntegerObject(5)

    assert int_obj.data_type() == ObjectType.INTEGER
    assert int_obj.inspect() == "5"
    assert int_obj.inspect() == str(int_obj)
    assert int_obj == IntegerObject(5)
    assert int_obj != 5


@pytest.mark.parametrize("bool_value", [True, False])
def test_boolean_object(bool_value):
    bool_obj = BooleanObject(bool_value)

    assert bool_obj.data_type() == ObjectType.BOOLEAN
    assert bool_obj.inspect() == str(bool_value).lower()
    assert bool_obj.inspect() == str(bool_obj).lower()
    assert bool_obj == BooleanObject(bool_value)
    assert bool_obj != bool_value


def test_null_object():
    null_obj = NullObject()

    assert null_obj.data_type() == ObjectType.NULL
    assert null_obj.inspect() == "NULL"
    assert null_obj.inspect() == str(null_obj)
    assert null_obj == NullObject()
    assert null_obj != "NULL"


@pytest.mark.parametrize(
    "wrapped_object",
    [
        BooleanObject(True),
        IntegerObject(10),
        NullObject(),
    ],
)
def test_return_object(wrapped_object):
    ret_obj = ReturnObject(wrapped_object)

    assert ret_obj.data_type() == ObjectType.RETURN
    assert ret_obj.inspect() == str(wrapped_object)
    assert ret_obj != wrapped_object


def test_function_object():
    parameters = [
        Identifier(Token(token_types.IDENTIFIER, "x"), "x"),
        Identifier(Token(token_types.IDENTIFIER, "y"), "y"),
    ]
    env = objs.Environment()

    summation = InfixExpression(
        Token(token_types.PLUS, "+"),
        Identifier(Token(token_types.IDENTIFIER, "x"), "x"),
        token_types.PLUS,
        Identifier(Token(token_types.IDENTIFIER, "y"), "y"),
    )
    ret_statement = ReturnStatement(
        Token(token_types.RETURN, "return"),
        summation,
    )
    body = BlockStatement(Token(token_types.LBRACE, "{"), [ret_statement])

    func_obj = FunctionObject(parameters, body, env)

    assert func_obj.data_type() == ObjectType.FUNCTION
    assert func_obj.inspect() == "fn(x, y) {\nreturn (x + y);\n}"


def test_array_object():
    array_obj = ArrayObject(
        [
            IntegerObject(-3),
            BooleanObject(True),
            IntegerObject(10),
        ]
    )

    assert array_obj.data_type() == ObjectType.ARRAY
    assert array_obj.inspect() == "[-3, true, 10]"


def test_compiled_function_object():
    opcode = opcodes.OPCONSTANT
    operands = (2**16 - 2,)

    instructions = make_instruction(opcode, *operands)
    written_instructions = instructions_to_string(instructions)

    dummy_n_locals = 0
    dummy_n_arguments = 0
    compiled_function_obj = CompiledFunctionObject(instructions, dummy_n_locals, dummy_n_arguments)

    assert compiled_function_obj.data_type() == ObjectType.COMPILED_FUNCTION
    assert (
        compiled_function_obj.inspect()
        == f"COMPILED_FUNCTION[\n{written_instructions}\n][n_locals={dummy_n_locals}][n_arguments={dummy_n_arguments}]"
    )
