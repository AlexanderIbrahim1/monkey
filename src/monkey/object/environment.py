"""
This module contains the Environment class. It is a hash map that associates the name
of an object with the object itself.
"""

import dataclasses
from typing import Optional

from monkey.object.object import Object
from monkey.object.error_object import UnknownIdentifierErrorObject
from monkey.tokens import Literal


@dataclasses.dataclass
class Environment:
    store: dict[Literal, Object] = dataclasses.field(default_factory=dict)
    outer: Optional['Environment'] = None

    def get(self, name: Literal) -> Object:
        if (result := self.store.get(name, None)) is not None:
            return result

        if self.outer is not None:
            return self.outer.get(name)

        return UnknownIdentifierErrorObject(name)

    def set(self, name: Literal, obj: Object) -> Object:
        self.store[name] = obj
        return obj


def new_enclosed_environment(outer: Environment) -> Environment:
    return Environment(outer=outer)
