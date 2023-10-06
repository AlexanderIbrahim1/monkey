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
from monkey.tokens import token_constants
from monkey.tokens import token_types

from monkey.parser.expressions import Expression
from monkey.parser.expressions import BooleanLiteral
from monkey.parser.expressions import CallExpression
from monkey.parser.expressions import FailedExpression
from monkey.parser.expressions import FunctionLiteral
from monkey.parser.expressions import Identifier
from monkey.parser.expressions import IfExpression
from monkey.parser.expressions import InfixExpression
from monkey.parser.expressions import IntegerLiteral
from monkey.parser.expressions import PrefixExpression
from monkey.parser.parsing_functions import InfixParsingFunction
from monkey.parser.parsing_functions import PrefixParsingFunction
from monkey.parser.precedences import Precedence
from monkey.parser.precedences import PRECEDENCE_MAP
from monkey.parser.program import Program
from monkey.parser.statements import Statement
from monkey.parser.statements import BlockStatement
from monkey.parser.statements import ExpressionStatement
from monkey.parser.statements import FailedStatement
from monkey.parser.statements import LetStatement
from monkey.parser.statements import ReturnStatement

from monkey.parser.constants import FAIL_EXPR
from monkey.parser.constants import FAIL_STMT


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

        self._fill_prefix_parsing_fns()
        self._fill_infix_parsing_fns()

    @property
    def current_token(self) -> Token:
        return self._current_token

    @property
    def peek_token(self) -> Token:
        return self._peek_token

    def parse_program(self) -> Program:
        program = Program()

        if self._lexer.has_errors():
            self._errors.extend(self._lexer.errors())
        else:
            while self._current_token != token_constants.EOF_TOKEN:
                if (statement := self._parse_statement()) != FAIL_STMT:
                    program.append(statement)
                self._parse_next_token()

        program.add_error(self._errors)

        return program

    def append_error(self, message: str) -> None:
        self._errors.append(message)

    def errors(self) -> list[str]:
        return self._errors

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def _fill_infix_parsing_fns(self) -> None:
        # self._infix_parsing_fns[token_types.PLUS] = self._parse_infix_expression
        # self._infix_parsing_fns[token_types.MINUS] = self._parse_infix_expression
        # self._infix_parsing_fns[token_types.SLASH] = self._parse_infix_expression
        # self._infix_parsing_fns[token_types.ASTERISK] = self._parse_infix_expression
        # self._infix_parsing_fns[token_types.LT] = self._parse_infix_expression
        # self._infix_parsing_fns[token_types.GT] = self._parse_infix_expression
        # self._infix_parsing_fns[token_types.EQ] = self._parse_infix_expression
        # self._infix_parsing_fns[token_types.NOT_EQ] = self._parse_infix_expression
        self._infix_parsing_fns[token_types.LPAREN] = self._parse_call_expression

    def parse_next_token(self) -> None:
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()


    def _parse_call_expression(self, function: Expression) -> CallExpression | FailedExpression:
        if not (isinstance(function, FunctionLiteral) or isinstance(function, Identifier)):
            return FAIL_EXPR

        call_token = self._current_token

        arguments = self._parse_call_arguments()
        if FAIL_EXPR in arguments:
            return FAIL_EXPR

        return CallExpression(call_token, function, arguments)

    def _parse_call_arguments(self) -> list[Expression]:
        arguments: list[Expression] = []

        # case: there are no arguments, and you've hit ')'
        if self._peek_token_type_is(token_types.RPAREN):
            self._parse_next_token()
            return arguments

        self._parse_next_token()  # move past current '('

        next_arg = self._parse_expression(Precedence.LOWEST)
        if next_arg == FAIL_EXPR:
            return [FAIL_EXPR]
        arguments.append(next_arg)

        while self._peek_token_type_is(token_types.COMMA):
            self._parse_next_token()  # move past current argument that was just parsed
            self._parse_next_token()  # move past current comma

            next_arg = self._parse_expression(Precedence.LOWEST)
            if next_arg == FAIL_EXPR:
                return [FAIL_EXPR]
            arguments.append(next_arg)

        if not self._expect_peek_and_next(token_types.RPAREN):
            return [FAIL_EXPR]

        return arguments

    def expect_peek_and_next(self, ttype: TokenType) -> bool:
        if self._peek_token_type_is(ttype):
            self._parse_next_token()
            return True
        else:
            self._peek_error(ttype)
            return False

    def peek_error(self, ttype: TokenType) -> None:
        ttype_expected_str = str(ttype)
        ttype_found_str = str(self._peek_token.token_type)
        message = f"Expected next token to be {ttype_expected_str}, got {ttype_found_str} instead"

        self._errors.append(message)

    def current_token_type_is(self, ttype: TokenType) -> bool:
        return self._current_token.token_type == ttype

    def peek_token_type_is(self, ttype: TokenType) -> bool:
        return self._peek_token.token_type == ttype

    def current_token_precedence(self) -> Precedence:
        return PRECEDENCE_MAP.get(self._current_token.token_type, Precedence.LOWEST)

    def peek_token_precedence(self) -> Precedence:
        return PRECEDENCE_MAP.get(self._peek_token.token_type, Precedence.LOWEST)

    def is_end_of_block_statement(self) -> bool:
        is_rbrace = self._current_token_type_is(token_types.RBRACE)
        is_eof = self._current_token_type_is(token_types.EOF)

        return is_rbrace or is_eof

    def is_end_of_subexpression(self, precedence: Precedence) -> bool:
        is_semicolon = self._peek_token_type_is(token_types.SEMICOLON)
        next_precedence_too_high = precedence >= self._peek_token_precedence()

        return is_semicolon or next_precedence_too_high
