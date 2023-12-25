"""
This module contains functions that take a `Bytecode` instance (the output of a compilation),
extract the necessary data from them, and serializes that data into a single "executable" file.
This executable is something that the VM will run.
"""

import pickle
from pathlib import Path
from typing import Any
from typing import Union

from monkey.object.object_type import OBJECT_TYPE_DICT
import monkey.object as objs

from monkey.code import Instructions
from monkey.compiler import Bytecode

from monkey.serialize.custom_exceptions import SerializeError


CompiledFunctionConstant = tuple[Instructions, int, int]


def serialize_bytecode(bytecode: Bytecode, serialized_filepath: Path | str) -> None:
    data_to_serialize = []
    data_to_serialize.append(bytecode.instructions)

    for constant in bytecode.constants:
        data_to_serialize.append(_object_to_data(constant))

    with open(serialized_filepath, "wb") as fout:
        pickle.dump(data_to_serialize, fout)


def deserialize_bytecode(serialized_filepath: Path | str) -> Bytecode:
    with open(serialized_filepath, "rb") as fin:
        deserialized_data: list[Any] = pickle.load(fin)

    instructions: Instructions = deserialized_data[0]
    if not isinstance(instructions, Instructions):
        raise SerializeError("Error while deserializing the instructions.")

    constant_objects: list[objs.Object] = []

    if len(deserialized_data) > 1:
        for constant in deserialized_data[1:]:
            constant_objects.append(_data_to_object(constant))

    return Bytecode(instructions, constant_objects)


def _object_to_data(const_obj: objs.Object) -> Union[int, str, CompiledFunctionConstant]:
    # there are only three types of constants: integers, strings, and compiled function objects
    # - not even booleans are constants (they are dealt with using OPTRUE and OPFALSE)
    match const_obj:
        case objs.IntegerObject():
            return const_obj.value
        case objs.StringObject():
            return const_obj.value
        case objs.CompiledFunctionObject():
            return (const_obj.instructions, const_obj.n_locals, const_obj.n_arguments)
        case _:
            raise SerializeError(
                f"Cannot serialize an object of data type: {OBJECT_TYPE_DICT[const_obj.data_type()]}"
            )


def _data_to_object(
    constant: Any,
) -> Union[objs.IntegerObject, objs.StringObject, objs.CompiledFunctionObject]:
    match constant:
        case int():
            return objs.IntegerObject(constant)
        case str():
            return objs.StringObject(constant)
        case [Instructions(), int(), int()]:
            return objs.CompiledFunctionObject(constant[0], constant[1], constant[2])  # type: ignore
        case _:
            raise SerializeError(f"Cannot serialize the following object: {constant}")
