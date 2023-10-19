import dataclasses

from monkey.code import Instructions
from monkey.object import Object
from monkey.parser import ASTNode


@dataclasses.dataclass
class Compiler:
    instructions: Instructions = Instructions()
    constants: list[Object] = dataclasses.field(defaultfactory=list)


@dataclasses.dataclass
class Bytecode:
    """
    Container to hold the instructions that the compiler generated, and the constants
    that the compiler evaluated. Gets passed to the virtual machine.
    """
    instructions: Instructions
    constants: list[Object]


def bytecode_from_compiler(compiler: Compiler) -> Bytecode:
    return Bytecode(compiler.instructions, compiler.constants)


def compile(compiler: Compiler, node: ASTNode) -> None:
    pass
