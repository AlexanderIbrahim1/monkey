from monkey.parser.precedences import Precedence
import monkey.tokens.token_types as token_types
import monkey.parser.expressions as exprs
import monkey.parser.statements as stmts

from monkey.parser.parser.constants import FAIL_EXPR
from monkey.parser.parser.constants import FAIL_STMT
from monkey.parser.parser.constants import ParsingFunction
from monkey.parser.parser.parser import Parser
from monkey.parser.parser._parse_block_statement import parse_block_statement


def parse_if_expression(
    parser: Parser, parsing_fn: ParsingFunction
) -> exprs.IfExpression | exprs.FailedExpression:
    expr_token = parser.current_token

    # the condition has to lie within a pair of parentheses
    # - this covers the left side
    if not parser.expect_peek_and_next(token_types.LPAREN):
        parser.append_error("Unable to parse if-expression : left parenthesis around the condition")
        return FAIL_EXPR

    parser.parse_next_token()

    expr_condition = parsing_fn(parser, Precedence.LOWEST)
    if expr_condition == FAIL_EXPR:
        parser.append_error("Unable to parse the condition of the if-expression")
        return FAIL_EXPR

    # the condition has to lie within a pair of parentheses
    # - this covers the right side
    if not parser.expect_peek_and_next(token_types.RPAREN):
        parser.append_error("Unable to parse if-expression: right parenthesis around the condition")
        return FAIL_EXPR

    # the consequence has to lie within a pair of braces
    # - this covers the left side
    if not parser.expect_peek_and_next(token_types.LBRACE):
        parser.append_error("Unable to parse if-expression: left brace of the consequence")
        return FAIL_EXPR

    # the parsing of the block statement takes care of the right side
    consequence = parse_block_statement(parser, parsing_fn)
    if consequence == FAIL_STMT:
        parser.append_error("Unable to parse the consequence of the if-expression")
        return FAIL_EXPR

    if parser.peek_token_type_is(token_types.ELSE):
        parser.parse_next_token()

        # the alternative has to lie within a pair of braces
        # - this covers the left side
        if not parser.expect_peek_and_next(token_types.LBRACE):
            parser.append_error("Unable to parse if-expression: left brace of the alternative")
            return FAIL_EXPR

        # the parsing of the block statement takes care of the right side
        alternative = parse_block_statement(parser, parsing_fn)
        if consequence == FAIL_STMT:
            parser.append_error("Unable to parse the alternative of the if-expression")
            return FAIL_EXPR
    else:
        alternative = None

    # ignore reason: already checked for possibilities of FailedStatement and FailedExpression
    return exprs.IfExpression(expr_token, expr_condition, consequence, alternative)  # type: ignore
