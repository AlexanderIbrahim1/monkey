from monkey.parser.parser.parser import Parser
from monkey.parser.program import Program

from monkey.parser.parser._constants import FAIL_STMT
from monkey.parser.parser._parse_statement import parse_statement
from monkey.parser.parser._parse_expression import parse_expression


def parse_program(parser: Parser) -> Program:
    program = Program()

    while not (parser.has_errors() or parser.current_token_is_eof()):
        if (statement := parse_statement(parser, parse_expression)) != FAIL_STMT:
            program.append(statement)
        parser.parse_next_token()

    program.add_error(parser.errors)

    return program
