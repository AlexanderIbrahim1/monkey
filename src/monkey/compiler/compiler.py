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
from monkey.code import extract_opcode
from monkey.code import make_instruction
from monkey.code import DUMMY_ADDRESS
import monkey.code.opcodes as opcodes

from monkey.compiler.custom_exceptions import CompilationError
from monkey.compiler.emitted_instruction import EmittedInstruction
import monkey.compiler.emitted_instruction as emitted


class Compiler:
    def __init__(
        self,
        instructions: Optional[Instructions] = None,
        constants: Optional[list[Object]] = None,
    ) -> None:
        if instructions is None:
            self._instructions = Instructions()
        else:
            self._instructions = instructions

        if constants is None:
            self._constants = []
        else:
            self._constants = constants

        self._last_instruction = EmittedInstruction()
        self._second_last_instruction = EmittedInstruction()

    @property
    def last_instruction(self) -> EmittedInstruction:
        return self._last_instruction

    @property
    def second_last_instruction(self) -> EmittedInstruction:
        return self._second_last_instruction

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

        self._update_last_instructions(opcode, pos)

        return pos

    def remove_last_instruction(self) -> None:
        if not emitted.is_valid_emitted_instruction(self._last_instruction):
            raise CompilationError(
                "Cannot remove the last instruction; it isn't a valid one.\n"
                f"last instruction: {self._last_instruction}"
            )

        new_end_pos = self._last_instruction.position
        self._instructions = self._instructions[:new_end_pos]
        self._last_instruction = self._second_last_instruction

    def replace_instructions(self, new_instructions: Instructions, start_position: int) -> None:
        self._check_last_instruction_position(new_instructions, start_position)

        end_position = start_position + len(new_instructions)
        self._instructions[start_position:end_position] = new_instructions

    def replace_operand(self, position: int, *operands: int) -> None:
        new_opcode = extract_opcode(self._instructions, position)
        new_instructions = make_instruction(new_opcode, *operands)

        self.replace_instructions(new_instructions, position)

    def _update_last_instructions(self, opcode: Opcode, position: int) -> None:
        self._second_last_instruction = self._last_instruction
        self._last_instruction = EmittedInstruction(opcode, position)

    def _check_last_instruction_position(self, new_instructions: Instructions, start_position: int) -> None:
        last_replaced_position = start_position + len(new_instructions) - 1
        if last_replaced_position >= len(self._instructions):
            raise CompilationError(
                "Attempted to replace instructions beyond the last existing instruction.\n"
                f"len(instructions) = {len(self._instructions)}\n"
                f"start_position = {start_position}\n"
                f"len(new_instructions) = {len(new_instructions)}"
            )


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
            consequence_jump_instr_position = compiler.emit(opcodes.OPJUMPWHENFALSE, DUMMY_ADDRESS)

            # depending on the expression in the consequence, it might leave an extra OPPOP on the stack
            compile(compiler, node.consequence)
            if emitted.is_pop(compiler.last_instruction):
                compiler.remove_last_instruction()

            if node.alternative is None:
                # with no alternative, we set the jump target to after the consequence instructions, if condition is false
                consequence_jump_position = len(compiler.instructions)
                compiler.replace_operand(consequence_jump_instr_position, consequence_jump_position)
            else:
                # with an alternative, we must put a jump just before it (to maybe jump past it)
                alternative_jump_instr_position = compiler.emit(opcodes.OPJUMP, DUMMY_ADDRESS)

                # with an alternative, we leapfrog over the alternative's jump instruction, if condition is false
                consequence_jump_position = len(compiler.instructions)
                compiler.replace_operand(consequence_jump_instr_position, consequence_jump_position)

                # now compile the alternative and set the jump to just past it
                compile(compiler, node.alternative)
                if emitted.is_pop(compiler.last_instruction):
                    compiler.remove_last_instruction()

                alternative_jump_position = len(compiler.instructions)
                compiler.replace_operand(alternative_jump_instr_position, alternative_jump_position)

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
