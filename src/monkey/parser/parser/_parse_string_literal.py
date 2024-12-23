import monkey.parser.expressions as exprs

from monkey.parser.parser._constants import ParsingFunction
from monkey.parser.parser.parser import Parser


def parse_string_literal(parser: Parser, _: ParsingFunction) -> exprs.StringLiteral | exprs.FailedExpression:
    token = parser.current_token
    literal = parser.current_token.literal

    return exprs.StringLiteral(token, literal)
