import monkey.tokens.token_types as token_types
import monkey.parser.statements as stmts

from monkey.parser.parser.parser import Parser

from monkey.parser.parser._constants import FAIL_STMT
from monkey.parser.parser._constants import ParsingFunction

from monkey.parser.parser._parse_statement import parse_statement


def parse_block_statement(
    parser: Parser, parsing_fn: ParsingFunction
) -> stmts.BlockStatement | stmts.FailedStatement:
    """
    Keep parsing statements into a block statement until a '}' or an EOF is hit.
    """
    stmt_token = parser.current_token
    statements: list[stmts.Statement] = []

    parser.parse_next_token()
    while not parser.is_end_of_block_statement():
        stmt = parse_statement(parser, parsing_fn)

        if stmt == FAIL_STMT:
            if parser.current_token_type_is(token_types.SEMICOLON):
                parser.parse_next_token()
                continue
            else:
                return FAIL_STMT

        statements.append(stmt)
        parser.parse_next_token()

    return stmts.BlockStatement(stmt_token, statements)
