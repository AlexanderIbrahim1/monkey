"""
This module contains the constants that other parts of this project use.
"""

from monkey.tokens.token_types import Literal

from monkey.parser.expressions import FailedExpression
from monkey.parser.statements import FailedStatement


DEFAULT_LITERAL: Literal = ""
FAIL_EXPR = FailedExpression()
FAIL_STMT = FailedStatement()
