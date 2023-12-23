"""
This module contains the StackFrame class, responsible for holding the execution-relevant
information for a given scope.
"""

import dataclasses

import monkey.code as code
import monkey.object as objs


@dataclasses.dataclass
class StackFrame:
    closure: objs.ClosureObject
    _: dataclasses.KW_ONLY
    base_pointer: int
    instruction_pointer: int = -1

    @property
    def instructions(self) -> code.Instructions:
        return self.closure.function.instructions
