"""
This module contains the EmittedInstruction class, a POD-type that the Compiler
uses to hold particular instructions of interest.
"""

import dataclasses

from monkey.code import Opcode
import monkey.code.opcodes as opcodes

from monkey.compiler.constants import DUMMY_EMITTED_INSTRUCTION_POSITION


@dataclasses.dataclass
class EmittedInstruction:
    opcode: Opcode = opcodes.OPDUMMY
    position: int = DUMMY_EMITTED_INSTRUCTION_POSITION


def is_valid_emitted_instruction(inst: EmittedInstruction) -> bool:
    return inst.opcode != opcodes.OPDUMMY or inst.position != DUMMY_EMITTED_INSTRUCTION_POSITION


def is_pop(inst: EmittedInstruction) -> bool:
    return inst.opcode == opcodes.OPPOP
