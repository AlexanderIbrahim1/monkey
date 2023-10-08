"""
This module contains the precedences of operators in the Monkey language.
"""

from functools import total_ordering
from typing import Any

import enum


# NOTE: even though `enum.auto()` automatically assigns incrementing numbers to the
# enum variants, I decided to use integers instead of `enum.auto()` to make explicit
# the fact that there is an order to these variants
@total_ordering
class Precedence(enum.Enum):
    LOWEST = 0
    EQUALS = 1
    LESSGREATER = 2
    SUM = 3
    PRODUCT = 4
    PREFIX = 5
    CALL = 6
    INDEX = 7

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Precedence):
            return NotImplemented

        # NOTE: the variants of an enum class are implicitly stored in an attribute called `value`
        return self.value < other.value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Precedence):
            return NotImplemented

        return self.value == other.value
