"""
This module contains dictionaries that map the identifier provided in the Monkey
language to the constant representing the token type.
"""

from monkey.tokens.monkey_token import TokenType
from monkey.tokens import token_types

KEYWORD_TO_TOKEN: dict[str, TokenType] = {
    "fn": token_types.FUNCTION,
    "let": token_types.LET,
}
