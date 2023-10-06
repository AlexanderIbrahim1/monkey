import monkey.parser.expressions as exprs

from monkey.parser.parser.constants import FAIL_EXPR
from monkey.parser.parser.constants import ParsingFunction
from monkey.parser.parser.parser import Parser


def parse_integer_literal(
    parser: Parser, _: ParsingFunction
) -> exprs.IntegerLiteral | exprs.FailedExpression:
    token = parser.current_token
    literal = parser.current_token.literal

    try:
        int(literal)
        return exprs.IntegerLiteral(token, literal)
    except Exception:
        parser.append_error(f"Unable to parse '{literal}' as an integer.")
        return FAIL_EXPR
