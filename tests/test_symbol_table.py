from monkey.compiler import build_enclosed_symbol_table
from monkey.compiler import Symbol
from monkey.compiler import SymbolTable
from monkey.compiler import SymbolScope


def test_define():
    expected_a = Symbol("a", SymbolScope.GLOBAL, 0)
    expected_b = Symbol("b", SymbolScope.GLOBAL, 1)
    expected_c = Symbol("c", SymbolScope.LOCAL, 0)
    expected_d = Symbol("d", SymbolScope.LOCAL, 1)
    expected_e = Symbol("e", SymbolScope.LOCAL, 0)
    expected_f = Symbol("f", SymbolScope.LOCAL, 1)

    symbol_table = SymbolTable()
    actual_a = symbol_table.define("a")
    actual_b = symbol_table.define("b")

    nested_table0 = build_enclosed_symbol_table(symbol_table)
    actual_c = nested_table0.define("c")
    actual_d = nested_table0.define("d")

    nested_table1 = build_enclosed_symbol_table(nested_table0)
    actual_e = nested_table1.define("e")
    actual_f = nested_table1.define("f")

    assert expected_a == actual_a
    assert expected_b == actual_b
    assert expected_c == actual_c
    assert expected_d == actual_d
    assert expected_e == actual_e
    assert expected_f == actual_f


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


def test_resolve_local():
    global_table = SymbolTable()
    global_table.define("a")  # global level, entry 0
    global_table.define("b")  # global level, entry 1

    local_table = build_enclosed_symbol_table(global_table)
    local_table.define("c")  # local level, entry 0
    local_table.define("d")  # local level, entry 1

    assert local_table.resolve("a") == Symbol("a", SymbolScope.GLOBAL, 0)
    assert local_table.resolve("b") == Symbol("b", SymbolScope.GLOBAL, 1)
    assert local_table.resolve("c") == Symbol("c", SymbolScope.LOCAL, 0)
    assert local_table.resolve("d") == Symbol("d", SymbolScope.LOCAL, 1)


def test_nested_resolve_global_local_free():
    global_table = SymbolTable()
    global_table.define("a")  # global level, entry 0
    global_table.define("b")  # global level, entry 1

    local_table0 = build_enclosed_symbol_table(global_table)
    local_table0.define("c")  # local level, entry 0
    local_table0.define("d")  # local level, entry 1

    local_table1 = build_enclosed_symbol_table(local_table0)
    local_table1.define("e")  # local level, entry 0
    local_table1.define("f")  # local level, entry 1

    assert global_table.resolve("a") == Symbol("a", SymbolScope.GLOBAL, 0)
    assert global_table.resolve("b") == Symbol("b", SymbolScope.GLOBAL, 1)
    assert global_table.resolve("c") is None
    assert global_table.resolve("d") is None
    assert global_table.resolve("e") is None
    assert global_table.resolve("f") is None

    assert local_table0.resolve("a") == Symbol("a", SymbolScope.GLOBAL, 0)
    assert local_table0.resolve("b") == Symbol("b", SymbolScope.GLOBAL, 1)
    assert local_table0.resolve("c") == Symbol("c", SymbolScope.LOCAL, 0)
    assert local_table0.resolve("d") == Symbol("d", SymbolScope.LOCAL, 1)
    assert local_table0.resolve("e") is None
    assert local_table0.resolve("f") is None

    assert local_table1.resolve("a") == Symbol("a", SymbolScope.GLOBAL, 0)
    assert local_table1.resolve("b") == Symbol("b", SymbolScope.GLOBAL, 1)
    assert local_table1.resolve("c") == Symbol("c", SymbolScope.FREE, 0)
    assert local_table1.resolve("d") == Symbol("d", SymbolScope.FREE, 1)
    assert local_table1.resolve("e") == Symbol("e", SymbolScope.LOCAL, 0)
    assert local_table1.resolve("f") == Symbol("f", SymbolScope.LOCAL, 1)


def test_nested_resolve_builtin():
    """
    Make sure that the builtin functions always resolve to a symbol in the BUILTIN scope,
    no matter how many times the symbol table has been enclosed in another one.
    """
    global_table = SymbolTable()
    global_table.define_builtin("builtin0", 0)
    global_table.define_builtin("builtin1", 1)
    global_table.define_builtin("builtin2", 2)
    global_table.define_builtin("builtin3", 3)

    local_table0 = build_enclosed_symbol_table(global_table)
    local_table1 = build_enclosed_symbol_table(local_table0)

    assert global_table.resolve("builtin0") == Symbol("builtin0", SymbolScope.BUILTIN, 0)
    assert global_table.resolve("builtin1") == Symbol("builtin1", SymbolScope.BUILTIN, 1)
    assert global_table.resolve("builtin2") == Symbol("builtin2", SymbolScope.BUILTIN, 2)
    assert global_table.resolve("builtin3") == Symbol("builtin3", SymbolScope.BUILTIN, 3)

    assert local_table0.resolve("builtin0") == Symbol("builtin0", SymbolScope.BUILTIN, 0)
    assert local_table0.resolve("builtin1") == Symbol("builtin1", SymbolScope.BUILTIN, 1)
    assert local_table0.resolve("builtin2") == Symbol("builtin2", SymbolScope.BUILTIN, 2)
    assert local_table0.resolve("builtin3") == Symbol("builtin3", SymbolScope.BUILTIN, 3)

    assert local_table1.resolve("builtin0") == Symbol("builtin0", SymbolScope.BUILTIN, 0)
    assert local_table1.resolve("builtin1") == Symbol("builtin1", SymbolScope.BUILTIN, 1)
    assert local_table1.resolve("builtin2") == Symbol("builtin2", SymbolScope.BUILTIN, 2)
    assert local_table1.resolve("builtin3") == Symbol("builtin3", SymbolScope.BUILTIN, 3)


def test_resolve_unresolvable_free():
    """Make sure that unresolvable names don't get automatically resolved to `FREE`"""
    global_table = SymbolTable()
    global_table.define("a")  # global level, entry 0

    local_table0 = build_enclosed_symbol_table(global_table)
    local_table0.define("b")  # local level, entry 0

    local_table1 = build_enclosed_symbol_table(local_table0)
    local_table1.define("c")  # local level, entry 0
    local_table1.define("d")  # local level, entry 1

    assert local_table1.resolve("a") == Symbol("a", SymbolScope.GLOBAL, 0)
    assert local_table1.resolve("b") == Symbol("b", SymbolScope.FREE, 0)
    assert local_table1.resolve("c") == Symbol("c", SymbolScope.LOCAL, 0)
    assert local_table1.resolve("d") == Symbol("d", SymbolScope.LOCAL, 1)
    assert local_table1.resolve("e") is None
    assert local_table1.resolve("f") is None
