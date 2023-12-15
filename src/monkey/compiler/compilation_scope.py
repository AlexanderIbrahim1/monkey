"""
This module contains the CompilationScope class, which allows us to create a
sequence of instructions that are stored outside of the main instructions, but
can be accessed from the main instructions (or a parent scope).
"""

from monkey.code.code import Instructions

from monkey.compiler.emitted_instruction import EmittedInstruction


class CompilationScope:
    instructions: Instructions
    last_instruction: EmittedInstruction
    second_last_instruction: EmittedInstruction
