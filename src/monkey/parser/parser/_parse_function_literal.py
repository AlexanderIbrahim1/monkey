import monkey.tokens.token_types as token_types
import monkey.parser.expressions as exprs

from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._constants import FAIL_STMT
from monkey.parser.parser._constants import ParsingFunction
from monkey.parser.parser.parser import Parser
from monkey.parser.parser._parse_block_statement import parse_block_statement
from monkey.parser.parser._parse_identifier import parse_identifier


def parse_function_literal(
    parser: Parser, parsing_fn: ParsingFunction
) -> exprs.FunctionLiteral | exprs.FailedExpression:
    fn_token = parser.current_token

    # function argument list is introduced with '('
    if not parser.expect_peek_and_next(token_types.LPAREN):
        return FAIL_EXPR

    parameters = _parse_function_parameters(parser, parsing_fn)
    if FAIL_EXPR in parameters:
        return FAIL_EXPR

    # the body of the function is introduced with '{'
    if not parser.expect_peek_and_next(token_types.LBRACE):
        return FAIL_EXPR

    body = parse_block_statement(parser, parsing_fn)
    if body == FAIL_STMT:
        return FAIL_EXPR

    # ignore reason: already checked for possibilities of 'parameters' and 'body' being FailedExpression
    return exprs.FunctionLiteral(fn_token, parameters, body)  # type: ignore


def _parse_function_parameters(
    parser: Parser, parsing_fn: ParsingFunction
) -> list[exprs.Identifier | exprs.FailedExpression]:
    identifiers: list[exprs.Identifier | exprs.FailedExpression] = []

    # case: there are no parameters, and you've hit ')'
    if parser.peek_token_type_is(token_types.RPAREN):
        parser.parse_next_token()
        return identifiers

    parser.parse_next_token()  # move past current '('

    current_identifier = parse_identifier(parser, parsing_fn)
    identifiers.append(current_identifier)

    while parser.peek_token_type_is(token_types.COMMA):
        parser.parse_next_token()  # move past current identifier
        parser.parse_next_token()  # move past current comma
        current_identifier = parse_identifier(parser, parsing_fn)
        identifiers.append(current_identifier)

    if not parser.expect_peek_and_next(token_types.RPAREN):
        return [FAIL_EXPR]

    return identifiers
