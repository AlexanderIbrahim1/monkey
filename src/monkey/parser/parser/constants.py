"""
This module contains constants needed for other modules in this directory.
"""

from typing import Callable

from monkey.parser.precedences import Precedence
from monkey.parser.parser.parser import Parser
import monkey.parser.expressions as exprs
import monkey.parser.statements as stmts


FAIL_EXPR = exprs.FailedExpression()
FAIL_STMT = stmts.FailedStatement()
ParsingFunction = Callable[[Parser, Precedence], exprs.Expression]
