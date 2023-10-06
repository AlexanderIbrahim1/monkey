from monkey.parser.precedences import Precedence
import monkey.tokens.token_types as token_types
import monkey.parser.expressions as exprs

from monkey.parser.parser.constants import FAIL_EXPR
from monkey.parser.parser.constants import ParsingFunction
from monkey.parser.parser.parser import Parser


def parse_grouped_expression(
    parser: Parser, parsing_fn: ParsingFunction
) -> exprs.Expression | exprs.FailedExpression:
    parser.parse_next_token()  # we want to start parsing whatever comes after the LPARENS

    # parse everything that comes after this
    expr = parsing_fn(parser, Precedence.LOWEST)
    if expr == FAIL_EXPR:
        parser.append_error("Unable to parse a grouped expression")
        return FAIL_EXPR

    # the parsing should have ended at an RPARENS
    if not parser.expect_peek_and_next(token_types.RPAREN):
        parser.append_error(f"Could not find a right parentheses for the expression {expr}")
        return FAIL_EXPR

    return expr
