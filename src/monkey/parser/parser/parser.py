"""
This module contains the Parser class, which is responsible for constructing
the AST from a lexer.

NOTE: why are there both `self._current_token` and `self._peek_token` fields?
- the Parser turns groups of tokens into statements and expressions
- it may need to peek into future tokens to make decisions with the current tokens

NOTE: the overall functionality of the parser seems simple
- keep trying to parse statements/expressions from the current and immediate future tokens
- each time it gets a statement/expression, append it to the program AST
- repeat until there are no more statements and expressions
"""

from monkey.lexer import Lexer
from monkey.tokens import Token
from monkey.tokens import TokenType
from monkey.tokens import token_types

from monkey.parser.precedences import Precedence
from monkey.parser.precedences import PRECEDENCE_MAP


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._errors: list[str] = []

        if self._lexer.has_errors():
            self._errors.extend(self._lexer.errors())

        self._current_token = self._lexer.next_token()
        self._peek_token = self._lexer.next_token()

    @property
    def current_token(self) -> Token:
        return self._current_token

    @property
    def peek_token(self) -> Token:
        return self._peek_token

    def append_error(self, message: str) -> None:
        self._errors.append(message)

    @property
    def errors(self) -> list[str]:
        return self._errors

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def parse_next_token(self) -> None:
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    def expect_peek_and_next(self, ttype: TokenType) -> bool:
        if self.peek_token_type_is(ttype):
            self.parse_next_token()
            return True
        else:
            self._peek_error(ttype)
            return False

    def current_token_precedence(self) -> Precedence:
        return PRECEDENCE_MAP.get(self._current_token.token_type, Precedence.LOWEST)

    def peek_token_precedence(self) -> Precedence:
        return PRECEDENCE_MAP.get(self._peek_token.token_type, Precedence.LOWEST)

    def current_token_type_is(self, ttype: TokenType) -> bool:
        return self._current_token.token_type == ttype

    def peek_token_type_is(self, ttype: TokenType) -> bool:
        return self._peek_token.token_type == ttype

    def current_token_is_eof(self) -> bool:
        return self._current_token.token_type == token_types.EOF

    def is_end_of_block_statement(self) -> bool:
        is_rbrace = self.current_token_type_is(token_types.RBRACE)
        is_eof = self.current_token_type_is(token_types.EOF)

        return is_rbrace or is_eof

    def is_end_of_subexpression(self, precedence: Precedence) -> bool:
        is_semicolon = self.peek_token_type_is(token_types.SEMICOLON)
        next_precedence_too_high = precedence >= self.peek_token_precedence()

        return is_semicolon or next_precedence_too_high

    def _peek_error(self, ttype: TokenType) -> None:
        ttype_expected_str = str(ttype)
        ttype_found_str = str(self._peek_token.token_type)
        message = f"Expected next token to be {ttype_expected_str}, got {ttype_found_str} instead"
        self._errors.append(message)
