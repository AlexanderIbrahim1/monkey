"""
This module contains the ObjectType enumeration, which represents the type of object
that an Object instance wraps around.

All possible types of objects in the Monkey language that the interpreter is capable of
understanding are described here.
"""


import enum


class ObjectType(enum.Enum):
    INTEGER = enum.auto()
    BOOLEAN = enum.auto()
    NULL = enum.auto()
    RETURN = enum.auto()
    ERROR = enum.auto()
    FUNCTION = enum.auto()
    STRING = enum.auto()
    BUILTIN = enum.auto()
    ARRAY = enum.auto()
    HASH = enum.auto()
    COMPILED_FUNCTION = enum.auto()
    CLOSURE = enum.auto()
    DEFAULT = enum.auto()


OBJECT_TYPE_DICT: dict[ObjectType, str] = {
    ObjectType.INTEGER: "INTEGER",
    ObjectType.BOOLEAN: "BOOLEAN",
    ObjectType.NULL: "NULL",
    ObjectType.RETURN: "RETURN",
    ObjectType.ERROR: "ERROR",
    ObjectType.FUNCTION: "FUNCTION",
    ObjectType.STRING: "STRING",
    ObjectType.BUILTIN: "BUILTIN",
    ObjectType.ARRAY: "ARRAY",
    ObjectType.HASH: "HASH",
    ObjectType.COMPILED_FUNCTION: "COMPILED_FUNCTION",
    ObjectType.CLOSURE: "CLOSURE",
    ObjectType.DEFAULT: "DEFAULT",
}
