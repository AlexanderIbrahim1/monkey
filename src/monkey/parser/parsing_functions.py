"""
This module contains the definitions for the parsing functions that are used in
the Pratt parser.

The definitions are set up such that both a function and a class that implements
the `__call__()` method can be used.
"""

from typing import Callable

from monkey.parser.expressions import Expression

PrefixParsingFunction = Callable[[], Expression]
InfixParsingFunction = Callable[[Expression], Expression]