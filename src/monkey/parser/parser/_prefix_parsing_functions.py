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

from monkey.parser.parser._parse_identifier import parse_identifier
from monkey.parser.parser._parse_integer_literal import parse_integer_literal
from monkey.parser.parser._parse_boolean_literal import parse_boolean_literal
from monkey.parser.parser._parse_prefix_expression import parse_prefix_expression
from monkey.parser.parser._parse_grouped_expression import parse_grouped_expression
from monkey.parser.parser._parse_if_expression import parse_if_expression
from monkey.parser.parser._parse_function_literal import parse_function_literal
from monkey.parser.parser._parse_string_literal import parse_string_literal

PrefixParsingFunction = Callable[[Parser, ParsingFunction], exprs.Expression]

PREFIX_PARSING_FUNCTIONS: dict[TokenType, PrefixParsingFunction] = {
    token_types.IDENTIFIER: parse_identifier,
    token_types.INT: parse_integer_literal,
    token_types.TRUE: parse_boolean_literal,
    token_types.FALSE: parse_boolean_literal,
    token_types.BANG: parse_prefix_expression,
    token_types.MINUS: parse_prefix_expression,
    token_types.LPAREN: parse_grouped_expression,
    token_types.IF: parse_if_expression,
    token_types.FUNCTION: parse_function_literal,
    token_types.STRING: parse_string_literal,
}
