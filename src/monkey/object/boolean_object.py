"""
This module contains the BooleanObject class, which implements the Object abstract
class, and represents a boolean literal object during evaluation.
"""

from dataclasses import dataclass
from typing import Any

from monkey.object.object_type import ObjectType
from monkey.object.object import Object


@dataclass(frozen=True)
class BooleanObject(Object):
    value: bool

    def data_type(self) -> ObjectType:
        return ObjectType.BOOLEAN

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BooleanObject):
            return NotImplemented

        return self.value == other.value

    def __repr__(self) -> str:
        return f"{self.value}"
