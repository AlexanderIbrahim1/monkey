import monkey.tokens.token_types as token_types
import monkey.parser.expressions as exprs

from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._constants import ParsingFunction
from monkey.parser.parser.parser import Parser

from monkey.parser.parser._parse_expression_list import parse_expression_list


def parse_call_expression(
    parser: Parser, parsing_fn: ParsingFunction, function: exprs.Expression
) -> exprs.CallExpression | exprs.FailedExpression:
    if not (isinstance(function, exprs.Identifier) or isinstance(function, exprs.FunctionLiteral)):
        return FAIL_EXPR

    call_token = parser.current_token

    arguments = parse_expression_list(parser, parsing_fn, token_types.RPAREN)
    if FAIL_EXPR in arguments:
        return FAIL_EXPR

    return exprs.CallExpression(call_token, function, arguments)
