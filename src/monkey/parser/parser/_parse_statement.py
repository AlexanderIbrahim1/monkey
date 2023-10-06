import monkey.tokens.token_types as token_types
import monkey.parser.statements as stmts

from monkey.parser.parser.constants import ParsingFunction
from monkey.parser.parser.parser import Parser

from monkey.parser.parser._parse_let_statement import parse_let_statement
from monkey.parser.parser._parse_return_statement import parse_return_statement
from monkey.parser.parser._parse_expression_statement import parse_expression_statement


def parse_statement(parser: Parser, parsing_fn: ParsingFunction) -> stmts.Statement:
    curr_token_type = parser.current_token.token_type

    if curr_token_type == token_types.LET:
        return parse_let_statement(parser, parsing_fn)
    elif curr_token_type == token_types.RETURN:
        return parse_return_statement(parser, parsing_fn)
    else:
        return parse_expression_statement(parser, parsing_fn)
