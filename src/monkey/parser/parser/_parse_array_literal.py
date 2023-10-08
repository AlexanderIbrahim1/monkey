import monkey.tokens.token_types as token_types
import monkey.parser.expressions as exprs

from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._constants import ParsingFunction
from monkey.parser.parser.parser import Parser

from monkey.parser.parser._parse_expression_list import parse_expression_list


def parse_array_literal(
    parser: Parser, parsing_fn: ParsingFunction
) -> exprs.ArrayLiteral | exprs.FailedExpression:
    token = parser.current_token

    elements = parse_expression_list(parser, parsing_fn, token_types.RBRACKET)
    if FAIL_EXPR in elements:
        return FAIL_EXPR

    return exprs.ArrayLiteral(token, elements)
