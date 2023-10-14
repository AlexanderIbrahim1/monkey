from monkey.parser.precedences import Precedence
import monkey.tokens.token_types as token_types
import monkey.parser.expressions as exprs

from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._constants import ParsingFunction
from monkey.parser.parser.parser import Parser


def parse_hash_literal(parser: Parser, parsing_fn: ParsingFunction) -> exprs.Expression | exprs.HashLiteral:
    token = parser.current_token
    kv_pairs: list[tuple[exprs.Expression, exprs.Expression]] = []

    while not parser.peek_token_type_is(token_types.RBRACE):  # while not the closing brace
        parser.parse_next_token()

        key = parsing_fn(parser, Precedence.LOWEST)
        if key == FAIL_EXPR:
            parser.append_error("Unable to parse key of a key-value pair")
            return FAIL_EXPR

        if not parser.expect_peek_and_next(token_types.COLON):
            parser.append_error("Unable to find colon after key")
            return FAIL_EXPR

        parser.parse_next_token()
        value = parsing_fn(parser, Precedence.LOWEST)
        if value == FAIL_EXPR:
            parser.append_error("Unable to parse value of a key-value pair")
            return FAIL_EXPR

        if not _is_end_of_hash_literal(parser):
            return FAIL_EXPR

        kv_pairs.append((key, value))

    if not parser.expect_peek_and_next(token_types.RBRACE):
        parser.append_error("Hash literal does not end with '}'")
        return FAIL_EXPR

    return exprs.HashLiteral(token, kv_pairs)


def _is_end_of_hash_literal(parser: Parser) -> bool:
    if parser.peek_token_type_is(token_types.RBRACE):
        return True
    else:
        return parser.expect_peek_and_next(token_types.COMMA)
