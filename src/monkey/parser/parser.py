"""
This module contains the Parser class, which is responsible for constructing
the AST from a lexer.

NOTE: why are there both `self._current_token` and `self._peek_token` fields?
- the Parser turns groups of tokens into statements and expressions
- it may need to peek into future tokens to make decisions with the current tokens
"""

from typing import Optional

from monkey.lexer import Lexer
from monkey.parser.program import Program
from monkey.tokens import Token


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer

        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None

        self.parse_next_token()
        self.parse_next_token()

    def parse_program(self) -> Optional[Program]:
        # NOTE: returning `None` is temporary; it will return an actual Program instance later
        return None

    def parse_next_token(self) -> None:
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()
