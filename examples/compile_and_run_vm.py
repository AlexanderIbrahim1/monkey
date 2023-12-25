"""
This is a script used to try out the serializing and deserializing of the bytecode output
from the compiler.
"""

from pathlib import Path

from monkey import Lexer
from monkey import Parser
from monkey.parser.parser import parse_program

from monkey.serialize.serialize import serialize_bytecode
from monkey.serialize.serialize import deserialize_bytecode

from monkey.compiler import Bytecode
from monkey.compiler import bytecode_from_compiler
from monkey.compiler import Compiler
from monkey.compiler import compile

import monkey.virtual_machine as vm


def run_compiler(executable_file: Path | str, source: str) -> None:
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parse_program(parser)

    compiler = Compiler()
    compile(compiler, program)

    bytecode: Bytecode = bytecode_from_compiler(compiler)

    serialize_bytecode(bytecode, executable_file)


def run_virtual_machine(executable_file: Path | str) -> None:
    bytecode: Bytecode = deserialize_bytecode(executable_file)
    machine = vm.VirtualMachine(bytecode)
    vm.run(machine)


if __name__ == "__main__":
    source = """
    let x = 3;
    let y = 5;
    let z = x + y;
    puts(z);
    """

    executable_file = Path("prog.pickle")

    run_compiler(executable_file, source)
    run_virtual_machine(executable_file)
