import monkey.tokens.token_types as token_types
import monkey.parser.expressions as exprs

from monkey.parser.precedences import Precedence
from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._constants import ParsingFunction
from monkey.parser.parser.parser import Parser


def parse_call_expression(
    parser: Parser, parsing_fn: ParsingFunction, function: exprs.Expression
) -> exprs.CallExpression | exprs.FailedExpression:
    if not (isinstance(function, exprs.Identifier) or isinstance(function, exprs.FunctionLiteral)):
        return FAIL_EXPR

    call_token = parser.current_token

    arguments = _parse_call_arguments(parser, parsing_fn)
    if FAIL_EXPR in arguments:
        return FAIL_EXPR

    return exprs.CallExpression(call_token, function, arguments)


def _parse_call_arguments(
    parser: Parser,
    parsing_fn: ParsingFunction,
) -> list[exprs.Expression]:
    arguments: list[exprs.Expression] = []

    parser.parse_next_token()

    # case: there are no arguments, and you've hit ')'
    if parser.current_token_type_is(token_types.RPAREN):
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

    if not parser.expect_peek_and_next(token_types.RPAREN):
        return [FAIL_EXPR]

    return arguments


def _is_function_correct_type(function: exprs.Expression) -> bool:
    is_func_literal = isinstance(function, exprs.FunctionLiteral)
    is_identifier = isinstance(function, exprs.Identifier)

    return is_func_literal or is_identifier
