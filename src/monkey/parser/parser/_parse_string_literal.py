import monkey.tokens.token_types as token_types
import monkey.parser.expressions as exprs

from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._constants import ParsingFunction
from monkey.parser.parser.parser import Parser


def parse_string_literal(
    parser: Parser, _: ParsingFunction
) -> exprs.BooleanLiteral | exprs.FailedExpression:
    token = parser.current_token
    literal = parser.current_token.literal

    return exprs.StringLiteral(token, literal)
