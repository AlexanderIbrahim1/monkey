"""
This module contains the DefaultObject class, which implements the Object abstract
class, and represents a default object type.

There are cases where a concrete object instance needs to exist (such as when allocating
space ahead of time), and it saves a lot of book-keeping to just use a meaningless
instance of an object instead of keeping track of `None`.
"""

from dataclasses import dataclass
from typing import Any

from monkey.object.object_type import ObjectType
from monkey.object.object import Object


@dataclass(frozen=True)
class DefaultObject(Object):
    def data_type(self) -> ObjectType:
        return ObjectType.DEFAULT

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DefaultObject):
            return NotImplemented

        return True

    def __repr__(self) -> str:
        return "DEFAULT"
