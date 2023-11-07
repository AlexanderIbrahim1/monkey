"""
"""

from typing import Optional

import dataclasses
import enum


class SymbolScope(enum.Enum):
    GLOBAL = enum.auto()


@dataclasses.dataclass
class Symbol:
    name: str
    scope: SymbolScope
    index: int


class SymbolTable:
    def __init__(
        self,
        store: Optional[dict[str, Symbol]] = None,
        n_definitions: int = 0,
    ) -> None:
        if store is None:
            self._store: dict[str, Symbol] = {}
        else:
            self._store = store

        self._n_definitions = n_definitions

    @property
    def n_definitions(self) -> int:
        return self._n_definitions

    def define(self, name: str) -> Symbol:
        new_symbol = Symbol(name, SymbolScope.GLOBAL, self._n_definitions)
        self._store[name] = new_symbol
        self._n_definitions += 1

        return new_symbol

    def resolve(self, name: str) -> Optional[Symbol]:
        return self._store.get(name)
