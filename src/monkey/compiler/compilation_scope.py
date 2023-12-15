"""
This module contains the CompilationScope class, which allows us to create a
sequence of instructions that are stored outside of the main instructions, but
can be accessed from the main instructions (or a parent scope).
"""

import dataclasses

from monkey.code.code import Instructions

from monkey.compiler.emitted_instruction import EmittedInstruction


@dataclasses.dataclass
class CompilationScope:
    instructions: Instructions = dataclasses.field(default_factory=Instructions)
    last_instruction: EmittedInstruction = dataclasses.field(default_factory=EmittedInstruction)
    second_last_instruction: EmittedInstruction = dataclasses.field(default_factory=EmittedInstruction)
