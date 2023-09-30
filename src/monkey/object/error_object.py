"""
This module contains the ReturnObject class, which implements the Object abstract
class, and is used to helper handle user or internal errors, for example, wrong
operators or unsupported operations.
"""

from dataclasses import dataclass
from typing import Any

from monkey.tokens import Literal

from monkey.object.object_type import ObjectType
from monkey.object.object_type import OBJECT_TYPE_DICT
from monkey.object.object import Object


@dataclass(frozen=True)
class ErrorObject(Object):
    message: str

    def data_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ErrorObject):
            return NotImplemented

        return self.message == other.message

    def __repr__(self) -> str:
        return f"ERROR: {self.message}"


class TypeMismatchErrorObject(ErrorObject):
    def __init__(self, type0: ObjectType, type1: ObjectType, operator: Literal) -> None:
        type0_str = OBJECT_TYPE_DICT[type0]
        type1_str = OBJECT_TYPE_DICT[type1]
        err_msg = f"type mismatch: {type0_str} {operator} {type1_str}"

        super().__init__(err_msg)

        self._type0 = type0
        self._type1 = type1
        self._operator = operator

    @property
    def object_type0(self) -> ObjectType:
        return self._type0

    @property
    def object_type1(self) -> ObjectType:
        return self._type1

    @property
    def operator(self) -> Literal:
        return self._operator


class UnknownInfixOperatorErrorObject(ErrorObject):
    def __init__(self, type0: ObjectType, type1: ObjectType, operator: Literal) -> None:
        type0_str = OBJECT_TYPE_DICT[type0]
        type1_str = OBJECT_TYPE_DICT[type1]
        err_msg = f"unknown infix operator: {type0_str} {operator} {type1_str}"

        super().__init__(err_msg)

        self._type0 = type0
        self._type1 = type1
        self._operator = operator

    @property
    def object_type0(self) -> ObjectType:
        return self._type0

    @property
    def object_type1(self) -> ObjectType:
        return self._type1

    @property
    def operator(self) -> Literal:
        return self._operator


class UnknownPrefixOperatorErrorObject(ErrorObject):
    def __init__(self, type0: ObjectType, operator: Literal) -> None:
        type0_str = OBJECT_TYPE_DICT[type0]
        err_msg = f"unknown operator: {operator}{type0_str}"

        super().__init__(err_msg)

        self._type0 = type0
        self._operator = operator

    @property
    def object_type0(self) -> ObjectType:
        return self._type0

    @property
    def operator(self) -> Literal:
        return self._operator
