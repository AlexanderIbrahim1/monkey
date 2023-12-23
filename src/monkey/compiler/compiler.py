import dataclasses

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

from monkey.containers.fixed_stack import FixedStack

from monkey.compiler.constants import MAX_COMPILATION_SCOPE_STACK_SIZE
from monkey.compiler.custom_exceptions import CompilationError
from monkey.compiler.emitted_instruction import EmittedInstruction
import monkey.compiler.emitted_instruction as emitted
from monkey.compiler.scope_instructions import ScopeInstructions

import monkey.compiler.symbol_table as sym

KeyValueExpressionPair = tuple[exprs.Expression, exprs.Expression]


# The OPCLOSURE takes the number of free variables as one of its two operands;
# at this point in the development cycle, we haven't even implemented free
# variables, but we still need a stand-in value for our current tests (that do
# not use free variables at all)
DUMMY_NUMBER_OF_FREE_VARIABLES: int = 0


class Compiler:
    def __init__(self) -> None:
        self._constants: list[Object] = []

        self._compilation_scopes = FixedStack[ScopeInstructions](MAX_COMPILATION_SCOPE_STACK_SIZE)
        main_scope = ScopeInstructions()
        self._compilation_scopes.push(main_scope)

        self.symbol_table: sym.SymbolTable = sym.SymbolTable()
        for i, builtin_name in enumerate(objs.BUILTINS_DICT):
            self.symbol_table.define_builtin(builtin_name, i)

    @property
    def number_of_scopes(self) -> int:
        return self._compilation_scopes.size()

    @property
    def last_instruction(self) -> EmittedInstruction:
        return self._compilation_scopes.peek().last_instruction

    @property
    def second_last_instruction(self) -> EmittedInstruction:
        return self._compilation_scopes.peek().second_last_instruction

    @property
    def instructions(self) -> Instructions:
        return self._compilation_scopes.peek().instructions

    @property
    def constants(self) -> list[Object]:
        return self._constants

    @property
    def current_scope(self) -> ScopeInstructions:
        return self._compilation_scopes.peek()

    def enter_scope(self) -> None:
        new_scope = ScopeInstructions()
        self._compilation_scopes.push(new_scope)

        # a new scope has a different table of symbols
        self.symbol_table = sym.build_enclosed_symbol_table(self.symbol_table)

    def leave_scope(self) -> Instructions:
        current_scope = self._compilation_scopes.pop()

        # abandon the current symbol table for the parent symbol table as we go up as scope
        if self.symbol_table.outer_table is None:
            raise CompilationError("Unable to leave scope; already in the top scope")

        self.symbol_table = self.symbol_table.outer_table

        return current_scope.instructions

    def add_constant_and_get_position(self, const: Object) -> int:
        position = len(self._constants)
        self._constants.append(const)

        return position

    def add_instruction_and_get_position(self, instr: Instructions) -> int:
        position = len(self.current_scope.instructions)
        self.current_scope.instructions += instr

        return position

    def emit(self, opcode: Opcode, *operands: int) -> int:
        instruction = make_instruction(opcode, *operands)
        pos = self.add_instruction_and_get_position(instruction)

        self._update_last_instructions(opcode, pos)

        return pos

    def remove_last_instruction(self) -> None:
        scope = self.current_scope
        if not emitted.is_valid_emitted_instruction(scope.last_instruction):
            raise CompilationError(
                "Cannot remove the last instruction; it isn't a valid one.\n"
                f"last instruction: {scope.last_instruction}"
            )

        new_end_pos = scope.last_instruction.position
        scope.instructions = scope.instructions[:new_end_pos]
        scope.last_instruction = scope.second_last_instruction

    def replace_instructions(self, new_instructions: Instructions, start_position: int) -> None:
        self._check_last_instruction_position(new_instructions, start_position)

        end_position = start_position + len(new_instructions)
        self.current_scope.instructions[start_position:end_position] = new_instructions

    def replace_operand(self, position: int, *operands: int) -> None:
        new_opcode = extract_opcode(self.current_scope.instructions, position)
        new_instructions = make_instruction(new_opcode, *operands)

        self.replace_instructions(new_instructions, position)

    def replace_last_instruction_with(self, new_opcode: opcodes.Opcode, *new_operands: int) -> None:
        # need to replace instructions in two places; the "last instruction", as described in
        # the function name, but also the overall sequence of instructions!
        position = self.current_scope.last_instruction.position
        new_instructions = make_instruction(new_opcode, *new_operands)
        self.replace_instructions(new_instructions, position)

        self.current_scope.last_instruction.opcode = new_opcode

    def is_last_instruction_opcode(self, opcode: opcodes.Opcode) -> bool:
        return self.last_instruction.opcode == opcode

    def _update_last_instructions(self, opcode: Opcode, position: int) -> None:
        scope = self.current_scope
        scope.second_last_instruction = scope.last_instruction
        scope.last_instruction = EmittedInstruction(opcode, position)

    def _check_last_instruction_position(self, new_instructions: Instructions, start_position: int) -> None:
        scope = self.current_scope
        last_replaced_position = start_position + len(new_instructions) - 1
        if last_replaced_position >= len(scope.instructions):
            raise CompilationError(
                "Attempted to replace instructions beyond the last existing instruction.\n"
                f"len(instructions) = {len(scope.instructions)}\n"
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
        case exprs.StringLiteral():
            string = objs.StringObject(node.value)
            constant_position = compiler.add_constant_and_get_position(string)
            compiler.emit(opcodes.OPCONSTANT, constant_position)
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
            # the if-expression is laid out like the following:
            # ...
            # CONDITION
            # MAYBE JUMP
            # CONSEQUENCE
            # MANDATORY JUMP
            # [TARGET OF MAYBE JUMP; BUT DOES NOTHING ON ITS OWN]
            # ALTERNATIVE
            # [TARGET OF MANDATORY JUMP, BUT DOES NOTHING ON ITS OWN]
            # ...
            compile(compiler, node.condition)

            # instruction that determines where we jump if the condition isn't true
            consequence_jump_instr_position = compiler.emit(opcodes.OPJUMPWHENFALSE, DUMMY_ADDRESS)

            # if the condition is true, we don't jump, and instead continue to this bytecode
            # depending on the expression in the consequence, it might leave an extra OPPOP on the stack
            compile(compiler, node.consequence)
            if compiler.is_last_instruction_opcode(opcodes.OPPOP):
                compiler.remove_last_instruction()

            # if we didn't jump before, we have to now, past the bytecode for the alternative
            alternative_jump_instr_position = compiler.emit(opcodes.OPJUMP, DUMMY_ADDRESS)

            # if we jumped because the condition was false, it should be to here (so we don't hit the
            # alternative's jump instr)
            consequence_jump_position = len(compiler.instructions)
            compiler.replace_operand(consequence_jump_instr_position, consequence_jump_position)

            # the bytecode for the alternative should either be whatever it is, or NULL
            if node.alternative is None:
                compiler.emit(opcodes.OPNULL)
            else:
                compile(compiler, node.alternative)
                if compiler.is_last_instruction_opcode(opcodes.OPPOP):
                    compiler.remove_last_instruction()

            # if we didn't jump, and hit the OPJUMP instruction, it should be to here
            alternative_jump_position = len(compiler.instructions)
            compiler.replace_operand(alternative_jump_instr_position, alternative_jump_position)
        case stmts.LetStatement():
            compile(compiler, node.value)
            symbol = compiler.symbol_table.define(node.name.value)

            if symbol.scope == sym.SymbolScope.GLOBAL:
                compiler.emit(opcodes.OPSETGLOBAL, symbol.index)
            else:
                compiler.emit(opcodes.OPSETLOCAL, symbol.index)
        case exprs.Identifier():
            symbol = compiler.symbol_table.resolve(node.value)
            if symbol is None:
                raise CompilationError(f"undefined variable: {node.value}")

            match symbol.scope:
                case sym.SymbolScope.BUILTIN:
                    compiler.emit(opcodes.OPGETBUILTIN, symbol.index)
                case sym.SymbolScope.GLOBAL:
                    compiler.emit(opcodes.OPGETGLOBAL, symbol.index)
                case sym.SymbolScope.LOCAL:
                    compiler.emit(opcodes.OPGETLOCAL, symbol.index)
                case _:
                    raise CompilationError(f"Unreachable: invalid scope found: {symbol.scope}")
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
        case exprs.ArrayLiteral():
            for element in node.elements:
                compile(compiler, element)
            compiler.emit(opcodes.OPARRAY, len(node.elements))
        case exprs.HashLiteral():
            # NOTE: the HashLiteral type in the book used an actual hash in its data structure, and Go makes no
            # guarantees about the order of elements in a Go map. We use a list instead of a dict, and so we
            # don't run into the same possible ordering bugs that the authors in the Go book would; we can skip
            # that precaution entirely, and directly use the node's key-value pairs!
            for key, value in node.key_value_pairs:
                compile(compiler, key)
                compile(compiler, value)

            n_pairs = len(node.key_value_pairs)
            compiler.emit(opcodes.OPHASH, 2 * n_pairs)
        case exprs.IndexExpression():
            compile(compiler, node.container)
            compile(compiler, node.inside)
            compiler.emit(opcodes.OPINDEX)
        case exprs.FunctionLiteral():  # parameters, body
            # compile the body of the function in its own scope
            compiler.enter_scope()

            for param in node.parameters:
                compiler.symbol_table.define(param.value)

            compile(compiler, node.body)

            # covers the case of an implicit return (no return statement, so no ReturnStatement case)
            if compiler.is_last_instruction_opcode(opcodes.OPPOP):
                compiler.replace_last_instruction_with(opcodes.OPRETURNVALUE)

            if not compiler.is_last_instruction_opcode(opcodes.OPRETURNVALUE):
                compiler.emit(opcodes.OPRETURN)

            # get the number of locals here, before we switch symbol tables in `compiler.leave_scope()`
            n_arguments = len(node.parameters)
            n_locals = compiler.symbol_table.n_definitions - n_arguments

            instructions = compiler.leave_scope()

            # ensures that the emitted instructions are stored in a separate object after compilation
            compiled_function = objs.CompiledFunctionObject(instructions, n_locals, n_arguments)

            position = compiler.add_constant_and_get_position(compiled_function)
            compiler.emit(opcodes.OPCLOSURE, position, DUMMY_NUMBER_OF_FREE_VARIABLES)
        case stmts.ReturnStatement():  # value
            compile(compiler, node.value)
            compiler.emit(opcodes.OPRETURNVALUE)
        case exprs.CallExpression():  # function, arguments
            compile(compiler, node.function)

            # NOTE: I can't check that the number of arguments pass to the function matches
            # the number of parameters that the function accepts, at this section. This is
            # because the CallExpression doesn't just strictly hold a `FunctionLiteral`, it
            # can hold lots of other expressions (that will eventually be evaluated as functions)
            #
            # So the compiler simply doesn't have enough information; we can only do the check
            # at the VM level

            for arg in node.arguments:
                compile(compiler, arg)

            n_arguments = len(node.arguments)
            compiler.emit(opcodes.OPCALL, n_arguments)
        case _:
            raise CompilationError(f"Invalid node encountered: {node}")
