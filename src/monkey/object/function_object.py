"""
This module contains the FunctionObject class, which implements the Object abstract
class, and represents a function object during evaluation.
"""

from dataclasses import astuple
from dataclasses import dataclass
from typing import Any

from monkey.parser.expressions import Identifier
from monkey.parser.statements import BlockStatement

from monkey.object.object_type import ObjectType
from monkey.object.object import Object
from monkey.object.environment import Environment


@dataclass(frozen=True)
class FunctionObject(Object):
    parameters: list[Identifier]
    body: BlockStatement
    env: Environment

    def data_type(self) -> ObjectType:
        return ObjectType.FUNCTION

    def inspect(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FunctionObject):
            return NotImplemented

        return astuple(self) == astuple(other)

    def __repr__(self) -> str:
        param_list = ", ".join([str(p) for p in self.parameters])
        return f"fn({param_list}) {{\n{self.body}\n}}"
