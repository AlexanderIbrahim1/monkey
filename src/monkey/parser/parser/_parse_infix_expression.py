import monkey.parser.expressions as exprs

from monkey.parser.parser._constants import FAIL_EXPR
from monkey.parser.parser._constants import ParsingFunction
from monkey.parser.parser.parser import Parser


def parse_infix_expression(
    parser: Parser, parsing_fn: ParsingFunction, left_expr: exprs.Expression
) -> exprs.InfixExpression | exprs.FailedExpression:
    token = parser.current_token
    operator = parser.current_token.literal

    precedence = parser.current_token_precedence()
    parser.parse_next_token()
    right_expr = parsing_fn(parser, precedence)

    if right_expr == FAIL_EXPR:
        parser.append_error(f"Unable to parse infix expression involving {operator}")
        return FAIL_EXPR

    return exprs.InfixExpression(token, left_expr, operator, right_expr)
