"""
This module contains the SymbolTable class, a data structure that maps the names
of symbols to information that allows us to retrieve those symbols (such as their
index in the globals stack, or their name, etc.).
"""

from typing import Optional

import dataclasses
import enum


class SymbolScope(enum.Enum):
    BUILTIN = enum.auto()
    GLOBAL = enum.auto()
    LOCAL = enum.auto()


@dataclasses.dataclass
class Symbol:
    name: str
    scope: SymbolScope
    index: int


@dataclasses.dataclass
class SymbolTable:
    store: dict[str, Symbol] = dataclasses.field(default_factory=dict)
    outer_table: Optional["SymbolTable"] = None

    def __post_init__(self) -> None:
        self._n_nonbuiltin_definitions: int = 0

    @property
    def n_definitions(self) -> int:
        return self._n_nonbuiltin_definitions

    def define(self, name: str) -> Symbol:
        if self.outer_table is None:
            symbol_scope = SymbolScope.GLOBAL
        else:
            symbol_scope = SymbolScope.LOCAL

        new_symbol = Symbol(name, symbol_scope, self._n_nonbuiltin_definitions)
        self.store[name] = new_symbol
        self._n_nonbuiltin_definitions += 1

        return new_symbol

    def define_builtin(self, name: str, index: int) -> Symbol:
        new_symbol = Symbol(name, SymbolScope.BUILTIN, index)
        self.store[name] = new_symbol

        return new_symbol

    def resolve(self, name: str) -> Optional[Symbol]:
        symbol = self.store.get(name)

        # if the symbol couldn't be found locally, recursively try higher scopes
        if symbol is None and self.outer_table is not None:
            symbol = self.outer_table.resolve(name)

        return symbol


def build_enclosed_symbol_table(outer_table: SymbolTable) -> SymbolTable:
    s = SymbolTable()
    s.outer_table = outer_table

    return s
