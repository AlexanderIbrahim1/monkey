"""
This module contains the SymbolTable class, a data structure that maps the names
of symbols to information that allows us to retrieve those symbols (such as their
index in the globals stack, or their name, etc.).
"""

from typing import Optional

import dataclasses
import enum

from monkey.compiler.constants import DUMMY_FUNCTION_SCOPE_INDEX


class SymbolScope(enum.Enum):
    BUILTIN = enum.auto()
    FREE = enum.auto()
    FUNCTION = enum.auto()
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
    free_symbols: list[Symbol] = dataclasses.field(default_factory=list)

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

    def define_function_name(self, name: str) -> Symbol:
        # the actual index of the symbol doesn't matter; we only use the fact that the symbol
        # has FUNCTION scope to emit a particular opcode, which finds the correct index on its own
        new_symbol = Symbol(name, SymbolScope.FUNCTION, DUMMY_FUNCTION_SCOPE_INDEX)
        self.store[name] = new_symbol

        return new_symbol

    def define_free(self, original: Symbol) -> Symbol:
        self.free_symbols.append(original)

        free_index = len(self.free_symbols) - 1
        new_symbol = Symbol(original.name, SymbolScope.FREE, free_index)

        self.store[original.name] = new_symbol

        return new_symbol

    def resolve(self, name: str) -> Optional[Symbol]:
        symbol = self.store.get(name)

        # if the symbol couldn't be found locally, recursively try higher scopes
        if symbol is None and self.outer_table is not None:
            symbol = self.outer_table.resolve(name)

            if symbol is None:
                return symbol

            if symbol.scope == SymbolScope.LOCAL or symbol.scope == SymbolScope.FREE:
                free_symbol = self.define_free(symbol)
                return free_symbol

        return symbol


def build_enclosed_symbol_table(outer_table: SymbolTable) -> SymbolTable:
    s = SymbolTable()
    s.outer_table = outer_table

    return s
