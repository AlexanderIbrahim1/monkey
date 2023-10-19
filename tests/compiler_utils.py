"""
This module contains functions needed to help run the `test_compiler.py` file.
"""

from monkey import Lexer
from monkey import Parser
from monkey.parser.program import Program
from monkey.parser.parser import parse_program


def parse(monkey_code: str) -> Program:
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parse_program(parser)

    return program
