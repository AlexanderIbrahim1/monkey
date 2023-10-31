"""
This module contains functions needed to help run the `test_compiler.py` file.
"""

import functools
import itertools
from typing import Any
from typing import Sequence

from monkey import Lexer
from monkey import Parser
from monkey.parser.program import Program
from monkey.parser.parser import parse_program

import monkey.code as code
import monkey.object as objs


class CompilerTestCase:
    def __init__(
        self,
        input_text: str,
        expected_constants: tuple[Any, ...],
        instruction_pairs: Sequence[tuple[code.Opcode, tuple[int, ...]]],
    ) -> None:
        self.input_text = input_text
        self.instructions = concatenate_instructions(instruction_pairs)
        self.constants = [make_object(value) for value in expected_constants]


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
