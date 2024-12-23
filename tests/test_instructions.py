import pytest

from monkey.code import Instructions
from monkey.code import lookup_opcode_definition
from monkey.code import make_instruction
from monkey.code import make_instructions_from_opcode_operand_pairs
from monkey.code import instructions_to_string

import monkey.code.opcodes as opcodes


def test_make_instruction():
    opcode = opcodes.OPCONSTANT
    operands = (2**16 - 2,)

    expected_instruction = Instructions([ord(opcode), 255, 254])
    actual_instruction = make_instruction(opcode, *operands)

    assert expected_instruction == actual_instruction


@pytest.mark.parametrize(
    "instruction_pairs",
    [
        ([(opcodes.OPCONSTANT, (2**16 - 2,))]),
        ([(opcodes.OPCONSTANT, (1,)), (opcodes.OPCONSTANT, (2,))]),
        ([(opcodes.OPADD, ())]),
        ([(opcodes.OPPOP, ())]),
        ([(opcodes.OPADD, ()), (opcodes.OPCONSTANT, (2**16 - 2,))]),
        ([(opcodes.OPCONSTANT, (2**16 - 2,)), (opcodes.OPADD, ())]),
        ([(opcodes.OPADD, ()), (opcodes.OPPOP, ())]),
        ([(opcodes.OPADD, ()), (opcodes.OPSUB, ()), (opcodes.OPMUL, ()), (opcodes.OPDIV, ())]),
        ([(opcodes.OPTRUE, ()), (opcodes.OPFALSE, ())]),
        ([(opcodes.OPEQUAL, ())]),
        ([(opcodes.OPNOTEQUAL, ())]),
        ([(opcodes.OPGREATERTHAN, ())]),
        ([(opcodes.OPMINUS, ())]),
        ([(opcodes.OPBANG, ())]),
        ([(opcodes.OPCALL, (0,))]),
        ([(opcodes.OPRETURNVALUE, ())]),
        ([(opcodes.OPRETURN, ())]),
        ([(opcodes.OPSETLOCAL, (0,))]),
        ([(opcodes.OPGETLOCAL, (1,))]),
        ([(opcodes.OPSETGLOBAL, (0,))]),
        ([(opcodes.OPGETGLOBAL, (1,))]),
        ([(opcodes.OPCLOSURE, (1, 2))]),
    ],
)
def test_instruction_to_string(instruction_pairs):
    instructions = make_instructions_from_opcode_operand_pairs(instruction_pairs)
    formatted_instructions = instructions_to_string(instructions)
    token_pairs = formatted_instructions.split("\n")

    for instruction_pair, token_pair in zip(instruction_pairs, token_pairs):
        actual_opcode_name, actual_operands = extract_name_and_operands(token_pair)
        expected_opcode_name = lookup_opcode_definition(instruction_pair[0]).name
        expected_operands = instruction_pair[1]

        assert actual_opcode_name == expected_opcode_name
        assert actual_operands == expected_operands


# --- HELPER FUNCTIONS ---


def extract_name_and_operands(formatted_instruction: str) -> tuple[str, tuple[int, ...]]:
    tokens = formatted_instruction.split()
    opcode_name = tokens[0]
    operands = tuple([int(t) for t in tokens[1:]])

    return opcode_name, operands
