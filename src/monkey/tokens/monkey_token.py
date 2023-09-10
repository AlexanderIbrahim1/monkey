"""
This module contains the basic Token class for the lexer.

NOTE: I can't call this file `token.py`, because it causes an ImportError when using `black`
"""

from dataclasses import dataclass

from monkey.tokens.token_types import Literal
from monkey.tokens.token_types import TokenType


@dataclass
class Token:
    token_type: TokenType
    literal: Literal
