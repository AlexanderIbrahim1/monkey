import monkey.tokens.token_types as token_types
import monkey.parser.expressions as exprs
import monkey.parser.statements as stmts

from monkey.parser.precedences import Precedence
from monkey.parser.parser.parser import Parser

from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._constants import FAIL_STMT
from monkey.parser.parser._constants import ParsingFunction


def parse_let_statement(
    parser: Parser, parsing_fn: ParsingFunction
) -> stmts.LetStatement | stmts.FailedStatement:
    """
    A let statement has the format:

        let <identifier> = <expression>;

    or in an even more verbose fashion:

        <let> <identifier> <assign> <expression> <semicolon>
    """

    # handle the `<let>` part
    stmt_token = parser.current_token

    # handle the `<identifier>` part
    if not parser.expect_peek_and_next(token_types.IDENTIFIER):
        return FAIL_STMT

    stmt_identifier = exprs.Identifier(parser.current_token, parser.current_token.literal)

    # handle the `<assign>` part
    if not parser.expect_peek_and_next(token_types.ASSIGN):
        return FAIL_STMT

    parser.parse_next_token()

    # handle the `<expression>` part
    stmt_expr = parsing_fn(parser, Precedence.LOWEST)
    if stmt_expr == FAIL_EXPR:
        return FAIL_STMT

    if isinstance(stmt_expr, exprs.FunctionLiteral):
        stmt_expr.name = stmt_identifier.value

    # make sure there's a semicolon to end it
    if not parser.expect_peek_and_next(token_types.SEMICOLON):
        return FAIL_STMT

    return stmts.LetStatement(stmt_token, stmt_identifier, stmt_expr)
