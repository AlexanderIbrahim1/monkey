"""
This module contains the Lexer, which takes the source code and turns it into
Token instances for a later step in the interpreter.
"""

NULL_BYTE = b"\x00"


class Lexer:
    def __init__(self, text_input: str, *, suppress_init: bool = False) -> None:
        self._text_input = text_input
        self._max_size = len(self._text_input)
        self._position = 0
        self._read_position = 1
        self._char = NULL_BYTE

        if not suppress_init:
            self.read_char()

    def read_char(self) -> None:
        if self._read_position >= self._max_size:
            self._char = NULL_TYPE
        else:
            self._char = self._text_input[self._read_position]

        self._position = self._read_position
        self._read_position += 1
