"""
This module contains the BuiltinObject class, which implements the Object abstract
class, and represents a built-in function during evaluation of the AST.
"""

from dataclasses import astuple
from dataclasses import dataclass
from typing import Annotated
from typing import Any
from typing import Callable

from monkey.object.object_type import ObjectType
from monkey.object.object import Object


@dataclass(frozen=True)
class BuiltinObject(Object):
    name: str
    func: Callable[[Annotated[Any, "multiple arguments"]], Object]

    def data_type(self) -> ObjectType:
        return ObjectType.BUILTIN

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BuiltinObject):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        return f"[builtin function: {self.name}]"
