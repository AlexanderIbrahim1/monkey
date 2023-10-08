import monkey.tokens.token_types as token_types
import monkey.parser.expressions as exprs

from monkey.parser.precedences import Precedence
from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._constants import ParsingFunction
from monkey.parser.parser.parser import Parser


def parse_expression_list(
    parser: Parser,
    parsing_fn: ParsingFunction,
    end_grouping: token_types.TokenType,
) -> list[exprs.Expression]:
    arguments: list[exprs.Expression] = []

    parser.parse_next_token()

    # case: there are no arguments, and you've hit the R-version of the grouping token
    if parser.current_token_type_is(end_grouping):
        return arguments

    next_arg = parsing_fn(parser, Precedence.LOWEST)
    if next_arg == FAIL_EXPR:
        return [FAIL_EXPR]
    arguments.append(next_arg)

    while parser.peek_token_type_is(token_types.COMMA):
        parser.parse_next_token()  # move past current argument that was just parsed
        parser.parse_next_token()  # move past current comma

        next_arg = parsing_fn(parser, Precedence.LOWEST)
        if next_arg == FAIL_EXPR:
            return [FAIL_EXPR]
        arguments.append(next_arg)

    if not parser.expect_peek_and_next(end_grouping):
        return [FAIL_EXPR]

    return arguments
