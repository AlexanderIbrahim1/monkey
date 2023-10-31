import dataclasses
from typing import Optional

from monkey.object import Object
from monkey.parser import ASTNode
from monkey.parser import Program
from monkey.tokens import token_types
from monkey.tokens.reserved_identifiers import TRUE_IDENTIFIER

import monkey.object as objs
import monkey.parser.expressions as exprs
import monkey.parser.statements as stmts

from monkey.code import Instructions
from monkey.code import Opcode
from monkey.code import make_instruction
from monkey.code import DUMMY_ADDRESS
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
        case stmts.BlockStatement():
            for statement in node.statements:
                compile(compiler, statement)
        case exprs.IntegerLiteral():
            integer = objs.IntegerObject(int(node.value))
            constant_position = compiler.add_constant_and_get_position(integer)
            compiler.emit(opcodes.OPCONSTANT, constant_position)
        case exprs.BooleanLiteral():
            value = True if node.value == TRUE_IDENTIFIER else False
            if value:
                compiler.emit(opcodes.OPTRUE)
            else:
                compiler.emit(opcodes.OPFALSE)
        case exprs.PrefixExpression():
            compile(compiler, node.expr)
            match node.operator:
                case token_types.MINUS:
                    compiler.emit(opcodes.OPMINUS)
                case token_types.BANG:
                    compiler.emit(opcodes.OPBANG)
                case _:
                    raise CompilationError(f"Unknown operator for prefix expression: {node.operator}")
        case exprs.IfExpression():
            compile(compiler, node.condition)
            compiler.emit(opcodes.OPJUMPWHENFALSE, DUMMY_ADDRESS)
            compile(compiler, node.consequence)
        case exprs.InfixExpression():
            # NOTE: if I wanted a simpler solution, I would have just implemented an opcode for the less
            #       than operator; however, for pedagogical purposes the book wants to emphasize the ability
            #       for the compiler to reorder expressions, so I'll do that here, even if it is messier
            if node.operator == token_types.LT:
                compile(compiler, node.right)
                compile(compiler, node.left)
                compiler.emit(opcodes.OPGREATERTHAN)
                return

            compile(compiler, node.left)
            compile(compiler, node.right)
            match node.operator:
                case token_types.PLUS:
                    compiler.emit(opcodes.OPADD)
                case token_types.MINUS:
                    compiler.emit(opcodes.OPSUB)
                case token_types.ASTERISK:
                    compiler.emit(opcodes.OPMUL)
                case token_types.SLASH:
                    compiler.emit(opcodes.OPDIV)
                case token_types.EQ:
                    compiler.emit(opcodes.OPEQUAL)
                case token_types.NOT_EQ:
                    compiler.emit(opcodes.OPNOTEQUAL)
                case token_types.GT:
                    compiler.emit(opcodes.OPGREATERTHAN)
                case _:
                    raise CompilationError(f"Unknown operator for infix expression: {node.operator}")
        case _:
            raise CompilationError(f"Invalid node encountered: {node}")
