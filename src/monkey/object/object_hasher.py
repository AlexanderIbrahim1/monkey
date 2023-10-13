"""
This module contains the ObjectHasher class, which is responsible for generating
the hash keys for each object.
"""

from dataclasses import dataclass

from monkey.object.object import Object
from monkey.object.object_type import ObjectType
from monkey.object.boolean_object import BooleanObject
from monkey.object.integer_object import IntegerObject
from monkey.object.string_object import StringObject


# NOT HASHABLE:
# - ArrayObject
# - BuiltinObject
# - Environment
# - ErrorObject
# - FunctionObject
# - NullObject
# - ReturnObject

# NOTE: this leaves only Boolean, Integer, and String


@dataclass(frozen=True)
class ObjectHash:
    data_type: ObjectType
    value: int


def create_object_hash(obj: Object) -> ObjectHash:
    if isinstance(obj, BooleanObject):
        return _boolean_object_hash_key(obj)
    elif isinstance(obj, IntegerObject):
        return _integer_object_hash_key(obj)
    elif isinstance(obj, StringObject):
        return _string_object_hash_key(obj)
    else:
        return ObjectHash(ObjectType.ERROR, -1)


def _boolean_object_hash_key(obj: BooleanObject) -> ObjectHash:
    return ObjectHash(ObjectType.BOOLEAN, hash(obj.value))


def _integer_object_hash_key(obj: IntegerObject) -> ObjectHash:
    return ObjectHash(ObjectType.INTEGER, obj.value)


def _string_object_hash_key(obj: StringObject) -> ObjectHash:
    return ObjectHash(ObjectType.STRING, hash(obj.value))
