"""
This module contains the NullObject class, which implements the Object abstract
class, and represents a NULL type during evaluation of the AST.
"""

from dataclasses import dataclass
from typing import Any

from monkey.object.object_type import ObjectType
from monkey.object.object import Object


@dataclass(frozen=True)
class NullObject(Object):
    def data_type(self) -> ObjectType:
        return ObjectType.NULL

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, NullObject):
            return NotImplemented

        return True

    def __repr__(self) -> str:
        return "NULL"
