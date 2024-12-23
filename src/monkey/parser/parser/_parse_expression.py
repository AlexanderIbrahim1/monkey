from monkey.parser.precedences import Precedence
from monkey.parser.parser.parser import Parser
import monkey.parser.expressions as exprs

from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._prefix_parsing_functions import PREFIX_PARSING_FUNCTIONS
from monkey.parser.parser._infix_parsing_functions import INFIX_PARSING_FUNCTIONS


def parse_expression(parser: Parser, precedence: Precedence) -> exprs.Expression:
    ttype = parser.current_token.token_type
    prefix_parsing_fn = PREFIX_PARSING_FUNCTIONS.get(ttype, None)

    if prefix_parsing_fn is None:
        return FAIL_EXPR

    expr = prefix_parsing_fn(parser, parse_expression)
    if expr == FAIL_EXPR:
        return FAIL_EXPR

    while not parser.is_end_of_subexpression(precedence):
        peek_ttype = parser.peek_token.token_type
        infix_parsing_fn = INFIX_PARSING_FUNCTIONS.get(peek_ttype, None)

        if infix_parsing_fn is None:
            return FAIL_EXPR

        parser.parse_next_token()

        expr = infix_parsing_fn(parser, parse_expression, expr)
        if expr == FAIL_EXPR:
            return FAIL_EXPR

    return expr
