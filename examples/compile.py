"""
This script takes a file representing monkey source code, and compiles it into a
file that stores the bytecode from the compilation.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional
from typing import Sequence

from monkey import Lexer
from monkey import Parser
from monkey import Program
from monkey.parser.parser import parse_program

from monkey.serialize.constants import MONKEY_SOURCE_FILE_SUFFIX
from monkey.serialize.constants import MONKEY_BYTECODE_FILE_SUFFIX
from monkey.serialize.serialize import serialize_bytecode

from monkey.compiler import Bytecode
from monkey.compiler import bytecode_from_compiler
from monkey.compiler import Compiler
from monkey.compiler import compile


def make_lexer(source: str) -> Lexer:
    lexer = Lexer(source)

    if lexer.has_errors():
        errors = "\n".join([str(err) for err in lexer.errors()])
        raise RuntimeError(errors)

    return lexer


def make_parser(lexer: Lexer) -> Parser:
    parser = Parser(lexer)

    if parser.has_errors():
        errors = "\n".join([str(err) for err in parser.errors])
        raise RuntimeError(errors)

    return parser


def run_parser(parser: Parser) -> Program:
    program = parse_program(parser)
    if program.has_errors():
        errors = "\n".join([str(err) for err in program.errors()])
        raise RuntimeError(errors)

    return program


def run_compiler(executable_file: Path | str, source: str) -> None:
    lexer = make_lexer(source)
    parser = make_parser(lexer)
    program = run_parser(parser)

    compiler = Compiler()
    compile(compiler, program)

    bytecode: Bytecode = bytecode_from_compiler(compiler)

    serialize_bytecode(bytecode, executable_file)


def main(argv: Optional[Sequence[str]] = None) -> int:
    usage_message = "usage: python compile.py <source_filename>"

    parser = argparse.ArgumentParser(usage=usage_message)
    parser.add_argument("source_filename", type=str, help="monkey source code file")

    args = parser.parse_args(argv)

    source_filename = Path(args.source_filename)
    if source_filename.suffix != MONKEY_SOURCE_FILE_SUFFIX:
        raise RuntimeError(
            f"This compiler requires the source code file to end in `{MONKEY_SOURCE_FILE_SUFFIX}`."
        )

    with open(source_filename, "r") as fin:
        source_code = fin.read()

    executable_filename = Path(source_filename.stem).with_suffix(MONKEY_BYTECODE_FILE_SUFFIX)

    run_compiler(executable_filename, source_code)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
