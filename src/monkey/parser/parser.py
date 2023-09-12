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

from typing import Optional

from monkey.lexer import Lexer
from monkey.parser.program import Program
from monkey.parser.statements.statement import Statement
from monkey.tokens import Token
from monkey.tokens import token_constants
from monkey.tokens import token_types


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer

        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None

        self._parse_next_token()
        self._parse_next_token()

    def parse_program(self) -> Program:
        program = Program()

        while self._current_token != token_constants.EOF_TOKEN:
            if (statement := self._parse_statement()) is not None:  # TODO: implement
                program.append(statement)
            self._parse_next_token()

        return program

    def _parse_next_token(self) -> None:
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    def _parse_statement(self) -> Optional[Statement]:
        if self._current_token is None:
            raise RuntimeError(
                "Logical error, where the current token in the Parser is None while parsing"
            )

        curr_token_type = self._current_token.token_type

        # TODO: add more branches in the future
        if curr_token_type == token_types.LET:
            return self._parse_let_statement()
        else:
            return None

    def _parse_let_statement(self) -> Optional[Statement]:
        # TODO: continue implementing from page 41 of the book
        return None
