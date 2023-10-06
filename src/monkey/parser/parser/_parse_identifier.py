import monkey.parser.expressions as exprs

from monkey.parser.parser.constants import ParsingFunction
from monkey.parser.parser.parser import Parser


def parse_identifier(parser: Parser, _: ParsingFunction) -> exprs.Identifier | exprs.FailedExpression:
    token = parser.current_token
    literal = parser.current_token.literal

    return exprs.Identifier(token, literal)
