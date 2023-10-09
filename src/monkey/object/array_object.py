"""
This module contains the ArrayObject class, which implements the Object abstract
class, and represents the result of evaluating an ArrayLiteral.
"""

from dataclasses import astuple
from dataclasses import dataclass
from typing import Any

from monkey.object.object_type import ObjectType
from monkey.object.object import Object


@dataclass
class ArrayObject(Object):
    elements: list[Object]

    def data_type(self) -> ObjectType:
        return ObjectType.ARRAY

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ArrayObject):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        elem_str = ", ".join([str(p) for p in self.elements])
        return f"[{elem_str}]"
