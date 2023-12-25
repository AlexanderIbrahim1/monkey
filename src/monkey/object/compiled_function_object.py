"""
This module contains the CompiledFunctionObject class, which implements the Object abstract
class, and represents a function which has already been compiled. As opposed to the FunctionObject
type, this class holds bytecode instructions that have already been compiled.
"""

from dataclasses import astuple
from dataclasses import dataclass
from typing import Any

from monkey.code.code import Instructions
from monkey.code.byte_operations import instructions_to_string

from monkey.object.object_type import ObjectType
from monkey.object.object import Object


@dataclass(frozen=True)
class CompiledFunctionObject(Object):
    instructions: Instructions
    n_locals: int
    n_arguments: int

    def data_type(self) -> ObjectType:
        return ObjectType.COMPILED_FUNCTION

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CompiledFunctionObject):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        written_instructions = instructions_to_string(self.instructions)
        locals_line = f"[n_locals={self.n_locals}]"
        arguments_line = f"[n_arguments={self.n_arguments}]"
        return f"COMPILED_FUNCTION {{\n{written_instructions}\n{locals_line}\n{arguments_line}\n}}"
