"""
This module contains the StackFrame class, responsible for holding the execution-relevant
information for a given scope.
"""

import dataclasses

import monkey.code as code
import monkey.object as objs


@dataclasses.dataclass
class StackFrame:
    function: objs.CompiledFunctionObject
    instruction_pointer: int = 0

    @property
    def instructions(self) -> code.Instructions:
        return self.function.instructions
