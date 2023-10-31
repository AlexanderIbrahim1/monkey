"""
This module contains opcode-related functions used throughout the rest of the
compiler.
"""

from monkey.code.code import Instructions
from monkey.code.code import Opcode
from monkey.code.code import OPCODE_SIZE

from monkey.code.definitions import OpcodeDefinition
from monkey.code.definitions import is_undefined
from monkey.code.definitions import lookup_opcode_definition

from monkey.code.constants import MAXIMUM_ADDRESS_DIGITS


def extract_opcode(instructions: Instructions, position: int) -> Opcode:
    i_begin = position
    i_end = i_begin + OPCODE_SIZE

    return Opcode(instructions[i_begin:i_end])


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


def instructions_to_string(instructions: Instructions) -> str:
    formatted_instructions: list[str] = []

    # NOTE to dev: can't use enumerate; index `i` might jump forward by more than 1 each loop
    i = 0
    while i < len(instructions):
        opcode = extract_opcode(instructions, i)
        opcode_def = lookup_opcode_definition(opcode)
        if is_undefined(opcode_def):
            raise ValueError(f"Cannot look up the opcode definition of '{opcode[0]}'")

        operands, bytes_read = _read_operands(opcode_def, instructions[i + 1 :])

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

    if n_expected_operands == 0:
        return f"{definition.name:<16s}   " + " " * MAXIMUM_ADDRESS_DIGITS
    elif n_expected_operands == 1:
        return f"{definition.name:<16s}   {operands[0]:0>{MAXIMUM_ADDRESS_DIGITS}d}"
    else:
        raise ValueError(f"Unable to format an instruction with '{n_expected_operands}' operands.")
