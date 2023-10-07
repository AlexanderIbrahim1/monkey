import monkey.tokens.token_types as token_types
import monkey.parser.expressions as exprs

from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._constants import ParsingFunction
from monkey.parser.parser.parser import Parser


def parse_boolean_literal(
    parser: Parser, _: ParsingFunction
) -> exprs.BooleanLiteral | exprs.FailedExpression:
    token = parser.current_token
    literal = parser.current_token.literal

    if token.token_type not in [token_types.TRUE, token_types.FALSE]:
        parser.append_error(f"Unable to parse '{literal}' as a boolean.")
        return FAIL_EXPR

    return exprs.BooleanLiteral(token, literal)
