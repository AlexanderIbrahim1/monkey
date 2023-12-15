"""
This module contains _constants needed for other modules in this directory.
"""

from typing import Callable

from monkey.parser.precedences import Precedence
from monkey.parser.parser.parser import Parser
import monkey.parser.expressions as exprs
import monkey.parser.statements as stmts


FAIL_EXPR = exprs.FailedExpression()
EMPTY_EXPR = exprs.EmptyExpression()
FAIL_STMT = stmts.FailedStatement()
EMPTY_STMT = stmts.EmptyStatement()
ParsingFunction = Callable[[Parser, Precedence], exprs.Expression]
