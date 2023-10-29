"""
This module contains functions needed to help run the `test_compiler.py` file.
"""

import functools
from typing import Any
from typing import Sequence

from monkey import Lexer
from monkey import Parser
from monkey.parser.program import Program
from monkey.parser.parser import parse_program

import monkey.code as code
import monkey.object as objs


class CompilerInfixTestCase:
    def __init__(
        self,
        input_text: str,
        expected_constants: tuple[Any, ...],
        instruction_pairs: Sequence[tuple[code.Opcode, tuple[int, ...]]],
    ) -> None:
        self.input_text = input_text
        self.instructions = concatenate_instructions(instruction_pairs)
        self.constants = [make_object(value) for value in expected_constants]


class CompilerBooleanTestCase:
    def __init__(
        self,
        input_text: str,
        instruction_pairs: Sequence[tuple[code.Opcode, tuple[int, ...]]],
    ) -> None:
        self.input_text = input_text
        self.instructions = concatenate_instructions(instruction_pairs)


def parse(monkey_code: str) -> Program:
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parse_program(parser)

    return program


def concatenate_instructions(
    instruction_pairs: Sequence[tuple[code.Opcode, tuple[int, ...]]]
) -> code.Instructions:
    instructions = (code.make_instruction(opcode, *operands) for (opcode, operands) in instruction_pairs)
    concat_instructions = functools.reduce(lambda x, y: x + y, instructions)

    return concat_instructions


def make_object(value: Any) -> objs.Object:
    match value:
        case bool():
            return objs.BooleanObject(value)
        case int():
            return objs.IntegerObject(value)
        case _:
            raise RuntimeError(f"Got a value for which there is no corresponding objs.Object type: '{value}'")
