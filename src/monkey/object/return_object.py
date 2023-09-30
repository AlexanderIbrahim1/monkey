"""
This module contains the ReturnObject class, which implements the Object abstract
class, and is a wrapper around another object that gets returned.
"""

from dataclasses import dataclass
from typing import Any

from monkey.object.object_type import ObjectType
from monkey.object.object import Object


@dataclass(frozen=True)
class ReturnObject(Object):
    value: Object

    def data_type(self) -> ObjectType:
        return ObjectType.RETURN

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ReturnObject):
            return NotImplemented

        return self.value == other.value

    def __repr__(self) -> str:
        return f"{self.value}"
