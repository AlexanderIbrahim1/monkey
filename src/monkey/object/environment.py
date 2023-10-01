"""
This module contains the Environment class. It is a hash map that associates the name
of an object with the object itself.
"""

import dataclasses
from typing import Optional

from monkey.object.object import Object
from monkey.tokens import Literal


@dataclasses.dataclass
class Environment:
    store: dict[Literal, Object] = dataclasses.field(default_factory=dict)

    def get(self, name: Literal) -> Optional[Object]:
        return self.store.get(name, None)

    def set(self, name: Literal, obj: Object) -> Object:
        self.store[name] = obj
        return obj
