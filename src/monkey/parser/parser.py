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
from monkey.tokens import TokenType
from monkey.tokens import token_constants
from monkey.tokens import token_types

from monkey.parser.expressions import Identifier
from monkey.parser.parsing_functions import InfixParsingFunction
from monkey.parser.parsing_functions import PrefixParsingFunction
from monkey.parser.program import Program
from monkey.parser.statements import Statement
from monkey.parser.statements import LetStatement
from monkey.parser.statements import ReturnStatement


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._errors: list[str] = []

        first_token = self._lexer.next_token()
        second_token = self._lexer.next_token()

        self._current_token = first_token
        self._peek_token = second_token

        # NOTE: I'll just use `self._prefix_parsing_fns[token] = func` or whatever to
        #       update these; no need for special methods like the book uses
        self._prefix_parsing_fns: dict[TokenType, PrefixParsingFunction] = {}
        self._infix_parsing_fns: dict[TokenType, InfixParsingFunction] = {}

    def parse_program(self) -> Program:
        program = Program()

        while self._current_token != token_constants.EOF_TOKEN:
            if (statement := self._parse_statement()) is not None:
                program.append(statement)
            self._parse_next_token()

        return program

    def errors(self) -> list[str]:
        return self._errors

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def _parse_next_token(self) -> None:
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    def _parse_statement(self) -> Optional[Statement]:
        curr_token_type = self._current_token.token_type

        # TODO: add more branches in the future
        if curr_token_type == token_types.LET:
            return self._parse_let_statement()
        elif curr_token_type == token_types.RETURN:
            return self._parse_return_statement()
        else:
            return None

    # TODO: implement
    def _parse_let_statement(self) -> Optional[LetStatement]:
        """
        A let statement has the format:

            let <identifier> = <expression>;

        or in an even more verbose fashion:

            <let> <identifier> <assign> <expression> <semicolon>
        """

        # handle the `<let>` part
        stmt_token = self._current_token

        # handle the `<identifier>` part
        if not self._expect_peek_and_next(token_types.IDENTIFIER):
            return None

        stmt_identifier = Identifier(self._current_token, self._current_token.literal)

        # handle the `<assign>` part
        if not self._expect_peek_and_next(token_types.ASSIGN):
            return None

        # handle the `<expression>` and `<semicolon>` parts
        # TODO: skipping the expressions until we encounter a semicolon
        while not self._current_token_type_is(token_types.SEMICOLON):
            self._parse_next_token()

        # TODO: dummy expression until we get a real one later
        stmt_value = Identifier(self._current_token, self._current_token.literal)

        return LetStatement(stmt_token, stmt_identifier, stmt_value)

    # TODO: implement
    def _parse_return_statement(self) -> Optional[ReturnStatement]:
        """
        A return statement has the format:

            return <expression>;

        or in an even more verbose fashion:

            <return> <expression> <semicolon>
        """

        # handle the `<return>` part
        stmt_token = self._current_token

        # handle the `<expression>` and `<semicolon>` parts
        # TODO: skipping the expressions until we encounter a semicolon
        while not self._current_token_type_is(token_types.SEMICOLON):
            self._parse_next_token()

        # TODO: dummy expression until we get a real one later
        stmt_value = Identifier(self._current_token, self._current_token.literal)

        return ReturnStatement(stmt_token, stmt_value)

    def _expect_peek_and_next(self, ttype: TokenType) -> bool:
        if self._peek_token_type_is(ttype):
            self._parse_next_token()
            return True
        else:
            self._peek_error(token_types.IDENTIFIER)
            return False

    def _peek_error(self, ttype: TokenType) -> None:
        ttype_expected_str = str(ttype)
        ttype_found_str = str(self._peek_token.token_type)
        message = f"Expected next token to be {ttype_expected_str}, got {ttype_found_str} instead"

        self._errors.append(message)

    def _current_token_type_is(self, ttype: TokenType) -> bool:
        return self._current_token.token_type == ttype

    def _peek_token_type_is(self, ttype: TokenType) -> bool:
        return self._peek_token.token_type == ttype
