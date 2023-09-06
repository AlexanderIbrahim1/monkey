"""
This module contains the Lexer, which takes the source code and turns it into
Token instances for a later step in the interpreter.
"""

from monkey.tokens import Literal
from monkey.tokens import Token
from monkey.tokens import TokenType
from monkey.tokens import token_types

# NULL_BYTE = b"\x00"
NULL_CHAR = ""


class Lexer:
    def __init__(self, text_input: str) -> None:
        self._text_input = text_input
        self._max_size = len(self._text_input)
        self._position = -1
        self._read_position = 0
        self._char = NULL_CHAR

        self.read_char()

    def read_char(self) -> None:
        if self._read_position >= self._max_size:
            self._char = NULL_CHAR
        else:
            self._char = self._text_input[self._read_position]

        self._position = self._read_position
        self._read_position += 1

    def next_token(self) -> Token:
        # NOTE: the contents of this function seems to be temporary; it looks like they'll
        #       be replaced with something easier to work with

        c = self._char
        if c == '=':
            token = Token(token_types.ASSIGN, c)
        elif c == ';':
            token = Token(token_types.SEMICOLON, c)
        elif c == '(':
            token = Token(token_types.LPAREN, c)
        elif c == ')':
            token = Token(token_types.RPAREN, c)
        elif c == '{':
            token = Token(token_types.LBRACE, c)
        elif c == '}':
            token = Token(token_types.RBRACE, c)
        elif c == ',':
            token = Token(token_types.COMMA, c)
        elif c == '+':
            token = Token(token_types.PLUS, c)
        elif c == NULL_CHAR:
            token = Token(token_types.EOF, c)
        else:
            raise ValueError(f"Unable to create token. Char: {c}")

        self.read_char()

        return token
