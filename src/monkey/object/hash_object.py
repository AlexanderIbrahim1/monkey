"""
This module contains the HashObject class, which implements the Object abstract
class, and represents the result of evaluating a HashLiteral.
"""

from dataclasses import astuple
from dataclasses import dataclass
from typing import Any

from monkey.object.object_type import ObjectType
from monkey.object.object import Object
from monkey.object.object_hasher import ObjectHash


@dataclass(frozen=True)
class HashKeyValuePair:
    key: Object
    value: Object


@dataclass(frozen=True)
class HashObject(Object):
    pairs: dict[ObjectHash, HashKeyValuePair]

    def data_type(self) -> ObjectType:
        return ObjectType.HASH

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, HashObject):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        pairs_list = ", ".join([f"{hash_pair.key}: {hash_pair.value}" for hash_pair in self.pairs.values()])

        return f"{{{pairs_list}}}"
