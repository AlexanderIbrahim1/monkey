from monkey import Lexer
from monkey import Parser
from monkey.parser.program import Program
from monkey.parser.parser import parse_program
import monkey.object as objs


def program_and_env(monkey_code: str) -> tuple[Program, objs.Environment]:
    lexer = Lexer(monkey_code)
    parser = Parser(lexer)
    program = parse_program(parser)
    env = objs.Environment()

    return program, env
