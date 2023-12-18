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
    _: dataclasses.KW_ONLY
    base_pointer: int
    instruction_pointer: int = -1

    @property
    def instructions(self) -> code.Instructions:
        return self.function.instructions


def default_stack_frame_factory() -> StackFrame:
    # A factory function to create a default stack frame. This is separated from the
    # definition of the class, because a default stack frame doesn't really make logical
    # sense (what would a sensible default `CompiledFunctionObject` be?), and we should
    # avoid having users accidentally construct one.

    # However, we need a default stack frame when making space in the VM's frame stack,
    # so we need some way of creating one
    default_function = objs.CompiledFunctionObject(code.Instructions(), 0)
    return StackFrame(default_function, base_pointer=0, instruction_pointer=0)
