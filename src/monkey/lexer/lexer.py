"""
This module contains the Lexer, which takes the source code and turns it into
Token instances for a later step in the interpreter.
"""

from monkey.tokens import Token
from monkey.tokens import TokenType
from monkey.tokens import token_maps
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

        self._skip_whitespace()

        flag_read_char = True

        c = self._char
        if c == "=":
            token = Token(token_types.ASSIGN, c)
        elif c == ";":
            token = Token(token_types.SEMICOLON, c)
        elif c == "(":
            token = Token(token_types.LPAREN, c)
        elif c == ")":
            token = Token(token_types.RPAREN, c)
        elif c == "{":
            token = Token(token_types.LBRACE, c)
        elif c == "}":
            token = Token(token_types.RBRACE, c)
        elif c == ",":
            token = Token(token_types.COMMA, c)
        elif c == "+":
            token = Token(token_types.PLUS, c)
        elif c == "-":
            token = Token(token_types.MINUS, c)
        elif c == "!":
            token = Token(token_types.BANG, c)
        elif c == "*":
            token = Token(token_types.ASTERISK, c)
        elif c == "/":
            token = Token(token_types.SLASH, c)
        elif c == "<":
            token = Token(token_types.LT, c)
        elif c == ">":
            token = Token(token_types.GT, c)
        elif _is_identifier_character(c):
            identifier = self._read_identifier()
            tok_type = _lookup_identifier_token_type(identifier)
            token = Token(tok_type, identifier)
            flag_read_char = False  # had to read 1 past the identifier to identify it; don't read again
        elif _is_digit_character(c):
            integer = self._read_number()
            token = Token(token_types.INT, integer)
            flag_read_char = (
                False  # had to read 1 past the number to identify it; don't read again
            )
        elif c == NULL_CHAR:
            token = Token(token_types.EOF, c)
        else:
            token = Token(token_types.ILLEGAL, c)

        if flag_read_char:
            self.read_char()

        return token

    def _read_identifier(self) -> str:
        start_position = self._position

        while _is_identifier_character(self._char):
            self.read_char()

        end_position = self._position

        identifier = self._text_input[start_position:end_position]

        return identifier

    def _read_number(self) -> str:
        start_position = self._position

        while _is_digit_character(self._char):
            self.read_char()

        end_position = self._position

        number = self._text_input[start_position:end_position]

        return number

    def _skip_whitespace(self) -> None:
        while self._char.isspace():
            self.read_char()


def _is_identifier_character(char: str) -> bool:
    return "a" <= char <= "z" or "A" <= char <= "Z" or char == "_"


def _is_digit_character(char: str) -> bool:
    return "0" <= char <= "9"


def _lookup_identifier_token_type(possible_keyword: str) -> TokenType:
    """
    Check if the identifier is one of the special reserved keywords, or if it
    is a user-defined identifier.
    """
    return token_maps.KEYWORD_TO_TOKEN.get(possible_keyword, token_types.IDENTIFIER)
