from monkey.code import Instructions
from monkey.code import make_instruction

import monkey.code.opcodes as opcodes


def test_make_instruction():
    opcode = opcodes.OPCONSTANT
    operands = (2**16 - 2,)

    expected_instruction = Instructions([ord(opcode), 255, 254])
    actual_instruction = make_instruction(opcode, *operands)

    assert expected_instruction == actual_instruction
