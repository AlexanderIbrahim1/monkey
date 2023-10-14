"""
This module contains different types of -ErrorObject classes. All of these implement
the Object abstract class. They are used to help handle user or internal errors.
"""

from dataclasses import dataclass
from dataclasses import astuple
from typing import Any

from monkey.tokens import Literal

from monkey.object.object_type import ObjectType
from monkey.object.object_type import OBJECT_TYPE_DICT
from monkey.object.object import Object


@dataclass(frozen=True)
class TypeMismatchErrorObject(Object):
    object_type0: ObjectType
    object_type1: ObjectType
    operator: Literal

    def data_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TypeMismatchErrorObject):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        type0_str = OBJECT_TYPE_DICT[self.object_type0]
        type1_str = OBJECT_TYPE_DICT[self.object_type1]
        return f"ERROR[type mismatch]: {type0_str} {self.operator} {type1_str}"


@dataclass(frozen=True)
class UnknownInfixOperatorErrorObject(Object):
    object_type0: ObjectType
    object_type1: ObjectType
    operator: Literal

    def data_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UnknownInfixOperatorErrorObject):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        type0_str = OBJECT_TYPE_DICT[self.object_type0]
        type1_str = OBJECT_TYPE_DICT[self.object_type1]
        return f"ERROR[unknown infix operator]: {type0_str} {self.operator} {type1_str}"


@dataclass(frozen=True)
class UnknownPrefixOperatorErrorObject(Object):
    object_type0: ObjectType
    operator: Literal

    def data_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UnknownPrefixOperatorErrorObject):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        type0_str = OBJECT_TYPE_DICT[self.object_type0]
        return f"ERROR[unknown prefix operator]: {self.operator}{type0_str}"


@dataclass(frozen=True)
class UnknownIdentifierErrorObject(Object):
    identifier: Literal

    def data_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UnknownIdentifierErrorObject):
            return NotImplemented

        return self.identifier == other.identifier

    def __repr__(self) -> str:
        return f"ERROR[unknown identifier]: {self.identifier}"


@dataclass(frozen=True)
class UnknownFunctionErrorObject(Object):
    object_type: ObjectType

    def data_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UnknownFunctionErrorObject):
            return NotImplemented

        return self.object_type == other.object_type

    def __repr__(self) -> str:
        type_str = OBJECT_TYPE_DICT[self.object_type]
        return f"ERROR[unknown function]: found {type_str}"


@dataclass(frozen=True)
class BuiltinErrorObject(Object):
    message: str

    def data_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BuiltinErrorObject):
            return NotImplemented

        return self.message == other.message

    def __repr__(self) -> str:
        return f"ERROR[builtin function]: {self.message}"


@dataclass(frozen=True)
class OutOfBoundsErrorObject(Object):
    container_type: ObjectType
    index: int
    size: int

    def data_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, OutOfBoundsErrorObject):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        type_str = OBJECT_TYPE_DICT[self.container_type]
        message_lines = [
            f"ERROR[index error]: invalid index access of instance of type '{type_str}'",
            f"                  : index: '{self.index}'                                ",
            f"                  : size: '{self.size }'                                 ",
        ]
        return "\n".join(message_lines)


@dataclass(frozen=True)
class InvalidIndexingErrorObject(Object):
    container_type: ObjectType
    inside_type: ObjectType

    def data_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, InvalidIndexingErrorObject):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        container_str = OBJECT_TYPE_DICT[self.container_type]
        inside_str = OBJECT_TYPE_DICT[self.inside_type]
        message_lines = [
            "ERROR[invalid index type]: invalid combination of container and index types",
            f"                         : container type: {container_str}                 ",
            f"                         : index type: {inside_str}                        ",
        ]
        return "\n".join(message_lines)


@dataclass(frozen=True)
class UnhashableTypeErrorObject(Object):
    attempted_type: ObjectType

    def data_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UnhashableTypeErrorObject):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        attempted_str = OBJECT_TYPE_DICT[self.attempted_type]
        return f"ERROR[unhashable type]: cannot hash object of type '{attempted_str}'"


@dataclass(frozen=True)
class KeyNotFoundErrorObject(Object):
    key: Object

    def data_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, KeyNotFoundErrorObject):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        return f"ERROR[key not found]: '{self.key}' not present in map"


def is_error_object(obj: Object):
    return obj.data_type() == ObjectType.ERROR
