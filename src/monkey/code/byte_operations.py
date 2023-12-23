"""
This module contains opcode-related functions used throughout the rest of the
compiler.
"""

import functools
from typing import Sequence

from monkey.code.code import Instructions
from monkey.code.code import Opcode
from monkey.code.code import OPCODE_SIZE

from monkey.code.definitions import OpcodeDefinition
from monkey.code.definitions import is_undefined
from monkey.code.definitions import lookup_opcode_definition

from monkey.code.constants import MAXIMUM_ADDRESS_DIGITS

from monkey.code.custom_types import OpcodeOperandPair


def extract_opcode(instructions: Instructions, position: int) -> Opcode:
    i_begin = position
    i_end = i_begin + OPCODE_SIZE

    return Opcode(instructions[i_begin:i_end])


def extract_operand(instructions: Instructions, position: int, operand_width: int) -> Instructions:
    i_begin = position
    i_end = i_begin + operand_width

    return instructions[i_begin:i_end]


def make_instruction(op: Opcode, *operands: int) -> Instructions:
    opcode_def = lookup_opcode_definition(op)
    if is_undefined(opcode_def):
        return Instructions()

    instruction_length = _instruction_length(opcode_def)

    mutable_instruction = bytearray(instruction_length)
    mutable_instruction[0] = ord(op)

    offset = 1
    for i, operand in enumerate(operands):
        width = opcode_def.operand_widths[i]
        instr_end = offset + width
        mutable_instruction[offset:instr_end] = operand.to_bytes(width, byteorder="big", signed=False)

        offset += width

    return Instructions(mutable_instruction)


def make_instructions_from_opcode_operand_pairs(
    instruction_pairs: Sequence[OpcodeOperandPair],
) -> Instructions:
    """
    Create a single instruction byte sequence from a sequence of pairs of opcodes
    and their corresponding operands.
    """
    instructions = (make_instruction(opcode, *operands) for (opcode, operands) in instruction_pairs)
    concat_instructions = functools.reduce(lambda x, y: x + y, instructions)

    return concat_instructions


def instructions_to_string(instructions: Instructions) -> str:
    formatted_instructions: list[str] = []

    # NOTE to dev: can't use enumerate; index `i` might jump forward by more than 1 each loop
    i = 0
    while i < len(instructions):
        opcode = extract_opcode(instructions, i)
        opcode_def = lookup_opcode_definition(opcode)
        if is_undefined(opcode_def):
            raise ValueError(f"Cannot look up the opcode definition of '{opcode[0]}'")

        operand_start_position = i + 1
        operands, bytes_read = _read_operands(opcode_def, instructions[operand_start_position:])

        # append the instructions to the string buffer
        formatted_instruction = _format_instruction(opcode_def, operands)
        formatted_instructions.append(formatted_instruction)

        next_opcode_steps = 1 + bytes_read
        i += next_opcode_steps

    return "\n".join(formatted_instructions)


def _read_operands(
    definition: OpcodeDefinition, remaining_instructions: Instructions
) -> tuple[list[int], int]:
    n_operands = len(definition.operand_widths)
    operands: list[int] = [0 for _ in range(n_operands)]

    offset = 0
    for i, width in enumerate(definition.operand_widths):
        instr_end = offset + width
        instruction = remaining_instructions[offset:instr_end]
        operands[i] = int.from_bytes(instruction, byteorder="big", signed=False)

        offset += width

    return operands, offset


def _instruction_length(definition: OpcodeDefinition) -> int:
    bytes_taken_by_opcode = 1
    bytes_taken_by_operands = sum(definition.operand_widths)
    return bytes_taken_by_opcode + bytes_taken_by_operands


def _format_instruction(definition: OpcodeDefinition, operands: list[int]) -> str:
    n_expected_operands = len(definition.operand_widths)

    if len(operands) != n_expected_operands:
        raise ValueError(
            "The number of operands read does not match the number expected for the opcode.\n"
            f"Expected operand widths: {n_expected_operands}\n"
            f"Found: {len(operands)}"
        )

    empty_space = " " * MAXIMUM_ADDRESS_DIGITS

    if n_expected_operands == 0:
        formatted_0 = empty_space
        formatted_1 = empty_space
    elif n_expected_operands == 1:
        formatted_0 = f"{operands[0]:0>{MAXIMUM_ADDRESS_DIGITS}d}"
        formatted_1 = empty_space
    elif n_expected_operands == 2:
        formatted_0 = f"{operands[0]:0>{MAXIMUM_ADDRESS_DIGITS}d}"
        formatted_1 = f"{operands[1]:0>{MAXIMUM_ADDRESS_DIGITS}d}"
    else:
        raise ValueError(f"Unable to format an instruction with '{n_expected_operands}' operands.")

    return f"{definition.name:<16s}   {formatted_0}   {formatted_1}"
