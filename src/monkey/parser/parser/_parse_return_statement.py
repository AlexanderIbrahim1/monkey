import monkey.tokens.token_types as token_types
import monkey.parser.statements as stmts

from monkey.parser.precedences import Precedence
from monkey.parser.parser.parser import Parser

from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._constants import FAIL_STMT
from monkey.parser.parser._constants import ParsingFunction


def parse_return_statement(
    parser: Parser, parsing_fn: ParsingFunction
) -> stmts.ReturnStatement | stmts.FailedStatement:
    """
    A return statement has the format:

        return <expression>;

    or in an even more verbose fashion:

        <return> <expression> <semicolon>
    """

    # handle the `<return>` part
    stmt_token = parser.current_token

    parser.parse_next_token()

    # handle the `<expression>` part
    stmt_expr = parsing_fn(parser, Precedence.LOWEST)
    if stmt_expr == FAIL_EXPR:
        return FAIL_STMT

    # make sure there's a semicolon to end it
    if not parser.expect_peek_and_next(token_types.SEMICOLON):
        return FAIL_STMT

    return stmts.ReturnStatement(stmt_token, stmt_expr)
