"""
This module contains opcode-related functions used throughout the rest of the
compiler.
"""

from monkey.code.code import Instructions
from monkey.code.code import Opcode

from monkey.code.definitions import OpcodeDefinition
from monkey.code.definitions import is_undefined
from monkey.code.definitions import lookup_opcode_definition


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
        if width == 2:
            _set_as_u16(mutable_instruction, offset, operand)
        else:
            assert False, "not implemented"

        offset += width

    return Instructions(mutable_instruction)


def _instruction_length(definition: OpcodeDefinition) -> int:
    bytes_taken_by_opcode = 1
    bytes_taken_by_operands = sum(definition.operand_widths)
    return bytes_taken_by_opcode + bytes_taken_by_operands


def _set_as_u16(instruction: bytearray, offset: int, operand: int) -> None:
    """
    Take the operand, interpret it as a 16-bit integer, and assign it to the
    instruction at `offset` and `offset + 1`.
    """
    first_8_bits = (operand >> 8) & 0xFF
    second_8_bits = operand & 0xFF

    instruction[offset] = first_8_bits
    instruction[offset + 1] = second_8_bits
