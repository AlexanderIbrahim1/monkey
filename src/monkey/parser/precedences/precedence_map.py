"""
This module contains a global constant dictionary that maps token constants to
their precedences.
"""

from monkey.tokens import TokenType
from monkey.tokens import token_types
from monkey.parser.precedences.precedences import Precedence

PRECEDENCE_MAP: dict[TokenType, Precedence] = {
    token_types.EQ: Precedence.EQUALS,
    token_types.NOT_EQ: Precedence.EQUALS,
    token_types.LT: Precedence.LESSGREATER,
    token_types.GT: Precedence.LESSGREATER,
    token_types.PLUS: Precedence.SUM,
    token_types.MINUS: Precedence.SUM,
    token_types.SLASH: Precedence.PRODUCT,
    token_types.ASTERISK: Precedence.PRODUCT,
}
