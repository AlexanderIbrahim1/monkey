"""
This module contains the SymbolTable class, a data structure that maps the names
of symbols to information that allows us to retrieve those symbols (such as their
index in the globals stack, or their name, etc.).
"""

from typing import Optional

import dataclasses
import enum


class SymbolScope(enum.Enum):
    LOCAL = enum.auto()
    GLOBAL = enum.auto()


@dataclasses.dataclass
class Symbol:
    name: str
    scope: SymbolScope
    index: int


@dataclasses.dataclass
class SymbolTable:
    store: dict[str, Symbol] = dataclasses.field(default_factory=dict)

    @property
    def n_definitions(self) -> int:
        return len(self.store)

    def define(self, name: str) -> Symbol:
        new_symbol = Symbol(name, SymbolScope.GLOBAL, self.n_definitions)
        self.store[name] = new_symbol

        return new_symbol

    def resolve(self, name: str) -> Optional[Symbol]:
        return self.store.get(name)
