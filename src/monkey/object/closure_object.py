"""
This module contains the ClosureObject class, which implements the Object abstract
class, and represents a function which has already been compiled, as well as the
free variables that it references within its body.
"""

from dataclasses import astuple
from dataclasses import dataclass
from typing import Any

from monkey.object.object_type import ObjectType
from monkey.object.object import Object
from monkey.object.compiled_function_object import CompiledFunctionObject


@dataclass(frozen=True)
class ClosureObject(Object):
    function: CompiledFunctionObject
    free_variables: list[Object]

    def data_type(self) -> ObjectType:
        return ObjectType.CLOSURE

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ClosureObject):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        function_section = f"FUNCTION:\n{self.function}"
        free_variables_section = "FREE VARIABLES:\n" + "\n".join([str(var) for var in self.free_variables])

        return f"CLOSURE:\n{function_section}\n{free_variables_section}"
