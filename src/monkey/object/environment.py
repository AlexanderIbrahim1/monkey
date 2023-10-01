"""
This module contains the Environment class. It is a hash map that associates the name
of an object with the object itself.
"""

import dataclasses

from monkey.object.object import Object
from monkey.object.error_object import UnknownIdentifierErrorObject
from monkey.tokens import Literal


@dataclasses.dataclass
class Environment:
    store: dict[Literal, Object] = dataclasses.field(default_factory=dict)

    def get(self, name: Literal) -> Object:
        return self.store.get(name, UnknownIdentifierErrorObject(name))

    def set(self, name: Literal, obj: Object) -> Object:
        self.store[name] = obj
        return obj
