"""
This module contains the precedences of operators in the Monkey language.
"""

import enum


# NOTE: even though `enum.auto()` automatically assigns incrementing numbers to the
# enum variants, I decided to use integers instead of `enum.auto()` to make explicit
# the fact that there is an order to these variants
class Precedence(enum.Enum):
    LOWEST = 0
    EQUALS = 1
    LESSGREATER = 2
    SUM = 3
    PRODUCT = 4
    PREFIX = 5
    CALL = 6
