from monkey.tokens import token_types
import monkey.parser.expressions as exprs

from monkey.parser.precedences import Precedence
from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._constants import ParsingFunction
from monkey.parser.parser.parser import Parser


def parse_index_expression(
    parser: Parser, parsing_fn: ParsingFunction, left_expr: exprs.Expression
) -> exprs.IndexExpression | exprs.FailedExpression:
    token = parser.current_token
    container = left_expr

    parser.parse_next_token()

    inside = parsing_fn(parser, Precedence.LOWEST)
    if inside == FAIL_EXPR:
        parser.append_error(f"Cannot parse inside of index expression of '{container}'")
        return FAIL_EXPR

    if not parser.expect_peek_and_next(token_types.RBRACKET):
        parser.append_error(f"Missing '{token_types.RBRACKET}' from index expression")
        return FAIL_EXPR

    return exprs.IndexExpression(token, container, inside)
