from monkey.code import Instructions
from monkey.code import lookup_opcode_definition
from monkey.code import make_instruction
from monkey.code import instructions_to_string

import monkey.code.opcodes as opcodes


def test_make_instruction():
    opcode = opcodes.OPCONSTANT
    operands = (2**16 - 2,)

    expected_instruction = Instructions([ord(opcode), 255, 254])
    actual_instruction = make_instruction(opcode, *operands)

    assert expected_instruction == actual_instruction


def test_instruction_to_string():
    opcode = opcodes.OPCONSTANT
    operands = (2**16 - 2,)
    instruction = make_instruction(opcode, *operands)

    formatted_instruction = instructions_to_string(instruction)
    tokens = formatted_instruction.split()
    actual_opcode = tokens[0]
    actual_operand = int(tokens[1])

    assert actual_opcode == lookup_opcode_definition(opcode).name
    assert actual_operand == operands[0]
