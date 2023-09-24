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

    def parse_program(self) -> Program:
        program = Program()

        if self._lexer.has_errors():
            err_msg = "Cannot parse. Lexer has errors."
            self._errors.append(err_msg)
            return program

        while self._current_token != token_constants.EOF_TOKEN:
            if (statement := self._parse_statement()) != FAIL_STMT:
                program.append(statement)
            self._parse_next_token()

        return program

    def errors(self) -> list[str]:
        return self._errors

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def _fill_prefix_parsing_fns(self) -> None:
        self._prefix_parsing_fns[token_types.IDENTIFIER] = self._parse_identifier
        self._prefix_parsing_fns[token_types.INT] = self._parse_integer_literal
        self._prefix_parsing_fns[token_types.BANG] = self._parse_prefix_expression
        self._prefix_parsing_fns[token_types.MINUS] = self._parse_prefix_expression
        self._prefix_parsing_fns[token_types.TRUE] = self._parse_boolean_literal
        self._prefix_parsing_fns[token_types.FALSE] = self._parse_boolean_literal
        self._prefix_parsing_fns[token_types.LPAREN] = self._parse_grouped_expression
        self._prefix_parsing_fns[token_types.IF] = self._parse_if_expression
        self._prefix_parsing_fns[token_types.FUNCTION] = self._parse_function_literal

    def _fill_infix_parsing_fns(self) -> None:
        self._infix_parsing_fns[token_types.PLUS] = self._parse_infix_expression
        self._infix_parsing_fns[token_types.MINUS] = self._parse_infix_expression
        self._infix_parsing_fns[token_types.SLASH] = self._parse_infix_expression
        self._infix_parsing_fns[token_types.ASTERISK] = self._parse_infix_expression
        self._infix_parsing_fns[token_types.LT] = self._parse_infix_expression
        self._infix_parsing_fns[token_types.GT] = self._parse_infix_expression
        self._infix_parsing_fns[token_types.EQ] = self._parse_infix_expression
        self._infix_parsing_fns[token_types.NOT_EQ] = self._parse_infix_expression
        self._infix_parsing_fns[token_types.LPAREN] = self._parse_call_expression

    def _parse_next_token(self) -> None:
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    def _parse_statement(self) -> Statement:
        curr_token_type = self._current_token.token_type

        if curr_token_type == token_types.LET:
            return self._parse_let_statement()
        elif curr_token_type == token_types.RETURN:
            return self._parse_return_statement()
        else:
            return self._parse_expression_statement()

    def _parse_let_statement(self) -> LetStatement | FailedStatement:
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
            return FAIL_STMT

        stmt_identifier = Identifier(self._current_token, self._current_token.literal)

        # handle the `<assign>` part
        if not self._expect_peek_and_next(token_types.ASSIGN):
            return FAIL_STMT

        self._parse_next_token()

        # handle the `<expression>` part
        stmt_expr = self._parse_expression(Precedence.LOWEST)
        if stmt_expr == FAIL_EXPR:
            return FAIL_STMT

        # make sure there's a semicolon to end it
        if not self._expect_peek_and_next(token_types.SEMICOLON):
            return FAIL_STMT

        return LetStatement(stmt_token, stmt_identifier, stmt_expr)

    def _parse_return_statement(self) -> ReturnStatement | FailedStatement:
        """
        A return statement has the format:

            return <expression>;

        or in an even more verbose fashion:

            <return> <expression> <semicolon>
        """

        # handle the `<return>` part
        stmt_token = self._current_token

        self._parse_next_token()

        # handle the `<expression>` part
        stmt_expr = self._parse_expression(Precedence.LOWEST)
        if stmt_expr == FAIL_EXPR:
            return FAIL_STMT

        # make sure there's a semicolon to end it
        if not self._expect_peek_and_next(token_types.SEMICOLON):
            return FAIL_STMT

        return ReturnStatement(stmt_token, stmt_expr)

    def _parse_expression_statement(self) -> ExpressionStatement | FailedStatement:
        stmt_token = self._current_token

        stmt_expr = self._parse_expression(Precedence.LOWEST)
        if stmt_expr == FAIL_EXPR:
            return FAIL_STMT

        return ExpressionStatement(stmt_token, stmt_expr)

    def _parse_block_statement(self) -> BlockStatement | FailedStatement:
        """
        Keep parsing statements into a block statement until a '}' or an EOF is hit.
        """
        stmt_token = self._current_token
        statements: list[Statement] = []

        self._parse_next_token()
        while not self._is_end_of_block_statement():
            stmt = self._parse_statement()

            if stmt == FAIL_STMT:
                return FAIL_STMT

            statements.append(stmt)
            self._parse_next_token()

        return BlockStatement(stmt_token, statements)

    def _parse_expression(self, precedence: Precedence) -> Expression:
        ttype = self._current_token.token_type
        parsing_fn = self._prefix_parsing_fns.get(ttype, None)

        if parsing_fn is None:
            return FAIL_EXPR

        expr = parsing_fn()
        if expr == FAIL_EXPR:
            return FAIL_EXPR

        while not self._is_end_of_subexpression(precedence):
            peek_ttype = self._peek_token.token_type
            infix_parsing_fn = self._infix_parsing_fns.get(peek_ttype, None)

            if infix_parsing_fn is None:
                return FAIL_EXPR

            self._parse_next_token()

            expr = infix_parsing_fn(expr)
            if expr == FAIL_EXPR:
                return FAIL_EXPR

        return expr

    def _parse_identifier(self) -> Identifier | FailedExpression:
        token = self._current_token
        literal = self._current_token.literal
        return Identifier(token, literal)

    def _parse_integer_literal(self) -> IntegerLiteral | FailedExpression:
        token = self._current_token
        literal = self._current_token.literal

        try:
            int(literal)
            return IntegerLiteral(token, literal)
        except Exception:
            self._errors.append(f"Unable to parse '{literal}' as an integer.")
            return FAIL_EXPR

    def _parse_boolean_literal(self) -> BooleanLiteral | FailedExpression:
        token = self._current_token
        literal = self._current_token.literal

        if token.token_type not in [token_types.TRUE, token_types.FALSE]:
            self._errors.append(f"Unable to parse '{literal}' as a boolean.")
            return FAIL_EXPR

        return BooleanLiteral(token, literal)

    def _parse_grouped_expression(self) -> Expression | FailedExpression:
        self._parse_next_token()  # we want to start parsing whatever comes after the LPARENS

        # parse everything that comes after this
        expr = self._parse_expression(Precedence.LOWEST)
        if expr == FAIL_EXPR:
            self._errors.append("Unable to parse a grouped expression")
            return FAIL_EXPR

        # the parsing should have ended at an RPARENS
        if not self._expect_peek_and_next(token_types.RPAREN):
            self._errors.append(f"Could not find a right parentheses for the expression {expr}")
            return FAIL_EXPR

        return expr

    def _parse_prefix_expression(self) -> PrefixExpression | FailedExpression:
        token = self._current_token
        operator = self._current_token.literal

        self._parse_next_token()
        expr = self._parse_expression(Precedence.PREFIX)

        if expr == FAIL_EXPR:
            self._errors.append(f"Unable to parse prefix expression beginning with {operator}")
            return FAIL_EXPR

        return PrefixExpression(token, operator, expr)

    def _parse_infix_expression(self, left_expr: Expression) -> InfixExpression | FailedExpression:
        token = self._current_token
        operator = self._current_token.literal

        precedence = self._current_token_precedence()
        self._parse_next_token()
        right_expr = self._parse_expression(precedence)

        if right_expr == FAIL_EXPR:
            self._errors.append(f"Unable to parse infix expression involving {operator}")
            return FAIL_EXPR

        return InfixExpression(token, left_expr, operator, right_expr)

    def _parse_if_expression(self) -> IfExpression | FailedExpression:
        expr_token = self._current_token

        # the condition has to lie within a pair of parentheses
        # - this covers the left side
        if not self._expect_peek_and_next(token_types.LPAREN):
            self._errors.append("Unable to parse if-expression : left parenthesis around the condition")
            return FAIL_EXPR

        self._parse_next_token()

        expr_condition = self._parse_expression(Precedence.LOWEST)
        if expr_condition == FAIL_EXPR:
            self._errors.append("Unable to parse the condition of the if-expression")
            return FAIL_EXPR

        # the condition has to lie within a pair of parentheses
        # - this covers the right side
        if not self._expect_peek_and_next(token_types.RPAREN):
            self._errors.append("Unable to parse if-expression: right parenthesis around the condition")
            return FAIL_EXPR

        # the consequence has to lie within a pair of braces
        # - this covers the left side
        if not self._expect_peek_and_next(token_types.LBRACE):
            self._errors.append("Unable to parse if-expression: left brace of the consequence")
            return FAIL_EXPR

        # the parsing of the block statement takes care of the right side
        consequence = self._parse_block_statement()
        if consequence == FAIL_STMT:
            self._errors.append("Unable to parse the consequence of the if-expression")
            return FAIL_EXPR

        if self._peek_token_type_is(token_types.ELSE):
            self._parse_next_token()

            # the alternative has to lie within a pair of braces
            # - this covers the left side
            if not self._expect_peek_and_next(token_types.LBRACE):
                self._errors.append("Unable to parse if-expression: left brace of the alternative")
                return FAIL_EXPR

            # the parsing of the block statement takes care of the right side
            alternative = self._parse_block_statement()
            if consequence == FAIL_STMT:
                self._errors.append("Unable to parse the alternative of the if-expression")
                return FAIL_EXPR
        else:
            alternative = None

        # ignore reason: already checked for possibilities of FailedStatement and FailedExpression
        return IfExpression(expr_token, expr_condition, consequence, alternative)  # type: ignore

    def _parse_function_literal(self) -> FunctionLiteral | FailedExpression:
        fn_token = self._current_token

        # function argument list is introduced with '('
        if not self._expect_peek_and_next(token_types.LPAREN):
            return FAIL_EXPR

        parameters = self._parse_function_parameters()
        if FAIL_EXPR in parameters:
            return FAIL_EXPR

        # the body of the function is introduced with '{'
        if not self._expect_peek_and_next(token_types.LBRACE):
            return FAIL_EXPR

        body = self._parse_block_statement()
        if body == FAIL_EXPR:
            return FAIL_EXPR

        # ignore reason: already checked for possibilities of 'parameters' and 'body' being FailedExpression
        return FunctionLiteral(fn_token, parameters, body)  # type: ignore

    def _parse_function_parameters(self) -> list[Identifier | FailedExpression]:
        identifiers: list[Identifier | FailedExpression] = []

        # case: there are no parameters, and you've hit ')'
        if self._peek_token_type_is(token_types.RPAREN):
            self._parse_next_token()
            return identifiers

        self._parse_next_token()  # move past current '('

        current_identifier = self._parse_identifier()
        identifiers.append(current_identifier)

        while self._peek_token_type_is(token_types.COMMA):
            self._parse_next_token()  # move past current identifier
            self._parse_next_token()  # move past current comma
            current_identifier = self._parse_identifier()
            identifiers.append(current_identifier)

        if not self._expect_peek_and_next(token_types.RPAREN):
            return [FAIL_EXPR]

        return identifiers

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

    def _expect_peek_and_next(self, ttype: TokenType) -> bool:
        if self._peek_token_type_is(ttype):
            self._parse_next_token()
            return True
        else:
            self._peek_error(ttype)
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

    def _current_token_precedence(self) -> Precedence:
        return PRECEDENCE_MAP.get(self._current_token.token_type, Precedence.LOWEST)

    def _peek_token_precedence(self) -> Precedence:
        return PRECEDENCE_MAP.get(self._peek_token.token_type, Precedence.LOWEST)

    def _is_end_of_block_statement(self) -> bool:
        is_rbrace = self._current_token_type_is(token_types.RBRACE)
        is_eof = self._current_token_type_is(token_types.EOF)

        return is_rbrace or is_eof

    def _is_end_of_subexpression(self, precedence: Precedence) -> bool:
        is_semicolon = self._peek_token_type_is(token_types.SEMICOLON)
        next_precedence_too_high = precedence >= self._peek_token_precedence()

        return is_semicolon or next_precedence_too_high
