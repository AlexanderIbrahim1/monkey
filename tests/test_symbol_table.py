from monkey.compiler import Symbol
from monkey.compiler import SymbolTable
from monkey.compiler import SymbolScope


def test_define():
    expected_a = Symbol("a", SymbolScope.GLOBAL, 0)
    expected_b = Symbol("b", SymbolScope.GLOBAL, 1)

    symbol_table = SymbolTable()
    actual_a = symbol_table.define("a")
    actual_b = symbol_table.define("b")

    assert expected_a == actual_a
    assert expected_b == actual_b


def test_resolve():
    symbol_table = SymbolTable()
    symbol_table.define("a")
    symbol_table.define("b")

    expected_a = Symbol("a", SymbolScope.GLOBAL, 0)
    expected_b = Symbol("b", SymbolScope.GLOBAL, 1)

    actual_a = symbol_table.resolve("a")
    assert actual_a is not None
    assert actual_a == expected_a

    actual_b = symbol_table.resolve("b")
    assert actual_b is not None
    assert actual_b == expected_b
