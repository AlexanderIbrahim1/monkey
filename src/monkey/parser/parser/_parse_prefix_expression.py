from monkey.parser.precedences import Precedence
import monkey.parser.expressions as exprs

from monkey.parser.parser.constants import FAIL_EXPR
from monkey.parser.parser.constants import ParsingFunction
from monkey.parser.parser.parser import Parser


def parse_prefix_expression(
    parser: Parser, parsing_fn: ParsingFunction
) -> exprs.PrefixExpression | exprs.FailedExpression:
    token = parser.current_token
    operator = parser.current_token.literal

    parser.parse_next_token()
    expr = parsing_fn(parser, Precedence.PREFIX)

    if expr == FAIL_EXPR:
        parser.append_error(f"Unable to parse prefix expression beginning with {operator}")
        return FAIL_EXPR

    return exprs.PrefixExpression(token, operator, expr)
