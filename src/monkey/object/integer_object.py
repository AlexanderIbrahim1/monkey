"""
This module contains the IntegerObject class, which implements the Object abstract
class, and represents an integer literal object during evaluation.
"""

from typing import Any

from monkey.object.object_type import ObjectType
from monkey.object.object import Object


class IntegerObject(Object):
    def __init__(self, value: int) -> None:
        self._value = value

    def data_type(self) -> ObjectType:
        return ObjectType.INTEGER

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, IntegerObject):
            return NotImplemented

        return self._value == other._value

    def __repr__(self) -> str:
        return f"{self._value}"
