import monkey.parser.statements as stmts

from monkey.parser.precedences import Precedence
from monkey.parser.parser.parser import Parser

from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._constants import FAIL_STMT
from monkey.parser.parser._constants import ParsingFunction


def parse_expression_statement(
    parser: Parser, parsing_fn: ParsingFunction
) -> stmts.ExpressionStatement | stmts.FailedStatement:
    stmt_token = parser.current_token

    stmt_expr = parsing_fn(parser, Precedence.LOWEST)
    if stmt_expr == FAIL_EXPR:
        return FAIL_STMT

    return stmts.ExpressionStatement(stmt_token, stmt_expr)
