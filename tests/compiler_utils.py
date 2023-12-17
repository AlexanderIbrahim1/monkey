"""
This module contains functions needed to help run the `test_compiler.py` file.
"""

import itertools
from typing import Any
from typing import Sequence

import pytest

from monkey import Lexer
from monkey import Parser
from monkey.parser.program import Program
from monkey.parser.parser import parse_program

import monkey.code as code
import monkey.object as objs

from monkey.compiler import bytecode_from_compiler
from monkey.compiler import Compiler
from monkey.compiler import compile


class CompilerTestCase:
    def __init__(
        self,
        input_text: str,
        expected_constants: tuple[Any, ...],
        instruction_pairs: Sequence[tuple[code.Opcode, tuple[int, ...]]],
    ) -> None:
        self.input_text = input_text
        self.instructions = code.make_instructions_from_opcode_operand_pairs(instruction_pairs)
        self.constants = [make_object(value) for value in expected_constants]


def perform_compiler_test_case(case: CompilerTestCase):
    """
    Assert that the input text in the case, when compiled, produces the expected
    bytecode instructions and constants.

    This method is so general for the test suite that all the tests end up using the
    same body, with very little to no variation. As a result, it becomes difficult to
    sort the different types of tests.

    By extracting the body of the testing code into its own function, we can separate
    the test cases into other functions with more descriptive names, allowing us to
    be better organized.
    """
    program = parse(case.input_text)
    compiler = Compiler()

    compile(compiler, program)
    bytecode = bytecode_from_compiler(compiler)

    try:
        assert bytecode.instructions == case.instructions
    except AssertionError:
        output = interleave_formatted_instructions(bytecode.instructions, case.instructions)
        pytest.fail(output)

    try:
        assert bytecode.constants == case.constants
    except AssertionError:
        output = f"""
            ACTUAL CONSTANTS
            {bytecode.constants}
            EXPECTED CONSTANTS
            {case.constants}
        """

        pytest.fail(output)


def parse(monkey_code: str) -> Program:
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parse_program(parser)

    return program


def make_object(value: Any) -> objs.Object:
    match value:
        case bool():
            return objs.BooleanObject(value)
        case int():
            return objs.IntegerObject(value)
        case str():
            return objs.StringObject(value)
        case (code.Instructions(), int()):
            # NOTE TO DEV [2023-12-17]: pyright thinks that `value` here is a sequence of
            # `code.Instructions | int`, instead of the first element being `code.Instructions`
            # and the second element being an `int`; I couldn't find a fix for this
            return objs.CompiledFunctionObject(value[0], value[1])  # type: ignore
        case None:
            return objs.NULL_OBJ
        case _:
            raise RuntimeError(f"Got a value for which there is no corresponding objs.Object type: '{value}'")


def interleave_formatted_instructions(
    instructions0: code.Instructions, instructions1: code.Instructions
) -> str:
    formatted0 = code.instructions_to_string(instructions0)
    lines0 = formatted0.split("\n")

    formatted1 = code.instructions_to_string(instructions1)
    lines1 = formatted1.split("\n")

    if len(lines0) == 0 and len(lines1) == 0:
        return ""

    padding = _get_line_padding(lines0, lines1)

    output = "\n".join(
        [
            f"{instr0} | {instr1}"
            for (instr0, instr1) in itertools.zip_longest(lines0, lines1, fillvalue=padding)
        ]
    )

    return f"\n{output}"


def _get_line_padding(lines0: list[str], lines1: list[str]) -> str:
    assert not (len(lines0) == 0 and len(lines1) == 0)

    if len(lines0) != 0:
        line_size = len(lines0[0])
    else:
        line_size = len(lines1[0])

    return " " * line_size
