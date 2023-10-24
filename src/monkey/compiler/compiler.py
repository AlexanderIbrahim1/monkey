import dataclasses
from typing import Optional

from monkey.code import Instructions
from monkey.object import Object
from monkey.parser import ASTNode
from monkey.parser import Program
from monkey.tokens import token_types

import monkey.object as objs
import monkey.parser.expressions as exprs
import monkey.parser.statements as stmts

from monkey.code import Opcode
from monkey.code import make_instruction
import monkey.code.opcodes as opcodes

from monkey.compiler.custom_exceptions import CompilationError


class Compiler:
    def __init__(
        self,
        instructions: Instructions = Instructions(),
        constants: Optional[list[Object]] = None,
    ) -> None:
        self._instructions = instructions

        if constants is None:
            self._constants = []
        else:
            self._constants = constants

    @property
    def instructions(self) -> Instructions:
        return self._instructions

    @property
    def constants(self) -> list[Object]:
        return self._constants

    def add_constant_and_get_position(self, const: Object) -> int:
        position = len(self._constants)
        self._constants.append(const)

        return position

    def add_instruction_and_get_position(self, instr: Instructions) -> int:
        position = len(self._instructions)
        self._instructions += instr

        return position

    def emit(self, opcode: Opcode, *operands: int) -> int:
        instruction = make_instruction(opcode, *operands)
        pos = self.add_instruction_and_get_position(instruction)

        return pos


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
    match node:
        case Program():
            for stmt in node.statements:
                compile(compiler, stmt)
        case stmts.ExpressionStatement():
            compile(compiler, node.value)
            compiler.emit(opcodes.OPPOP)  # don't want to keep the (unusable) result on the stack
        case exprs.IntegerLiteral():
            integer = objs.IntegerObject(int(node.value))
            constant_position = compiler.add_constant_and_get_position(integer)
            compiler.emit(opcodes.OPCONSTANT, constant_position)
        case exprs.InfixExpression():
            # TODO: split this to separate functions for handling integers, booleans, strings, etc.
            compile(compiler, node.left)
            compile(compiler, node.right)
            match node.operator:
                case token_types.PLUS:
                    compiler.emit(opcodes.OPADD)
                case _:
                    raise CompilationError(f"Unknown operator for infix expression: {node.operator}")
        case _:
            raise CompilationError(f"Invalid node encountered: {node}")
