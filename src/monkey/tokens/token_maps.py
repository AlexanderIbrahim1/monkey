"""
This module contains dictionaries that map the identifier provided in the Monkey
language to the constant representing the token type.
"""

from monkey.tokens import token_types
import monkey.tokens.reserved_identifiers as reserved

KEYWORD_TO_TOKEN: dict[str, token_types.TokenType] = {
    reserved.FUNCTION_IDENTIFIER: token_types.FUNCTION,
    reserved.LET_IDENTIFIER: token_types.LET,
    reserved.TRUE_IDENTIFIER: token_types.TRUE,
    reserved.FALSE_IDENTIFIER: token_types.FALSE,
    reserved.IF_IDENTIFIER: token_types.IF,
    reserved.ELSE_IDENTIFIER: token_types.ELSE,
    reserved.RETURN_IDENTIFIER: token_types.RETURN,
}
