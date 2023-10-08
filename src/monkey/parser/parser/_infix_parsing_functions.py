"""
This module contains the definitions for the parsing functions that are used in
the Pratt parser.

The definitions are set up such that both a function and a class that implements
the `__call__()` method can be used.
"""

from typing import Callable

from monkey.tokens import TokenType
from monkey.tokens import token_types
import monkey.parser.expressions as exprs

from monkey.parser.parser._constants import ParsingFunction
from monkey.parser.parser.parser import Parser

from monkey.parser.parser._parse_index_expression import parse_index_expression
from monkey.parser.parser._parse_infix_expression import parse_infix_expression
from monkey.parser.parser._parse_call_expression import parse_call_expression

InfixParsingFunction = Callable[[Parser, ParsingFunction, exprs.Expression], exprs.Expression]

INFIX_PARSING_FUNCTIONS: dict[TokenType, InfixParsingFunction] = {
    token_types.PLUS: parse_infix_expression,
    token_types.MINUS: parse_infix_expression,
    token_types.SLASH: parse_infix_expression,
    token_types.ASTERISK: parse_infix_expression,
    token_types.LT: parse_infix_expression,
    token_types.GT: parse_infix_expression,
    token_types.EQ: parse_infix_expression,
    token_types.NOT_EQ: parse_infix_expression,
    token_types.LPAREN: parse_call_expression,
    token_types.LBRACKET: parse_index_expression,
}
