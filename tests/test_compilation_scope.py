from monkey.code.code import Instructions
from monkey.code.byte_operations import make_instruction
import monkey.code.opcodes as opcodes

from monkey.compiler.compiler import Compiler
from monkey.compiler.compilation_scope import CompilationScope
from monkey.compiler.emitted_instruction import EmittedInstruction


class TestCompilerWithCompilationScopes:
    def test_basic(self) -> None:
        compiler = Compiler()
        assert compiler.number_of_scopes == 1

    def test_emit_one_instruction(self) -> None:
        compiler = Compiler()
        compiler.emit(opcodes.OPMUL)

        assert compiler.number_of_scopes == 1
        assert compiler.current_scope.instructions == make_instruction(opcodes.OPMUL)

    def test_enter_scope(self) -> None:
        compiler = Compiler()
        compiler.enter_scope()

        assert compiler.number_of_scopes == 2

    def test_emit_instruction_and_enter_scope(self) -> None:
        compiler = Compiler()
        compiler.emit(opcodes.OPMUL)

        assert compiler.number_of_scopes == 1
        assert compiler.current_scope.instructions == make_instruction(opcodes.OPMUL)

        compiler.enter_scope()

        assert compiler.number_of_scopes == 2
        assert compiler.current_scope.instructions == Instructions()

    def test_enter_scope_and_emit_instruction(self) -> None:
        compiler = Compiler()

        assert compiler.number_of_scopes == 1
        assert compiler.current_scope.instructions == Instructions()

        compiler.enter_scope()
        compiler.emit(opcodes.OPMUL)

        assert compiler.number_of_scopes == 2
        assert compiler.current_scope.instructions == make_instruction(opcodes.OPMUL)

    def test_emit_then_enter_scope_then_emit(self) -> None:
        compiler = Compiler()

        assert compiler.number_of_scopes == 1
        assert compiler.current_scope.instructions == Instructions()

        compiler.emit(opcodes.OPSUB)

        assert compiler.number_of_scopes == 1
        assert compiler.current_scope.instructions == make_instruction(opcodes.OPSUB)

        compiler.enter_scope()

        assert compiler.number_of_scopes == 2
        assert compiler.current_scope.instructions == Instructions()

        compiler.emit(opcodes.OPMUL)

        assert compiler.number_of_scopes == 2
        assert compiler.current_scope.instructions == make_instruction(opcodes.OPMUL)

    def test_enter_and_leave_scope(self) -> None:
        compiler = Compiler()
        assert compiler.number_of_scopes == 1

        compiler.enter_scope()
        assert compiler.number_of_scopes == 2

        compiler.leave_scope()
        assert compiler.number_of_scopes == 1

    def test_enter_two_scopes(self) -> None:
        compiler = Compiler()
        compiler.enter_scope()
        compiler.enter_scope()

        assert compiler.number_of_scopes == 3

    def test_emit_after_entering_and_leaving_scopes(self) -> None:
        opmul_instr = make_instruction(opcodes.OPMUL)
        opadd_instr = make_instruction(opcodes.OPADD)
        opsub_instr = make_instruction(opcodes.OPSUB)
        opmulsub_instr = opmul_instr + opsub_instr

        compiler = Compiler()

        compiler.emit(opcodes.OPMUL)

        assert compiler.number_of_scopes == 1
        assert compiler.current_scope.instructions == opmul_instr
        assert compiler.current_scope.last_instruction == EmittedInstruction(opcodes.OPMUL, 0)

        compiler.enter_scope()
        compiler.emit(opcodes.OPADD)

        assert compiler.number_of_scopes == 2
        assert compiler.current_scope.instructions == opadd_instr
        assert compiler.current_scope.last_instruction == EmittedInstruction(opcodes.OPADD, 0)

        compiler.leave_scope()

        assert compiler.number_of_scopes == 1
        assert compiler.current_scope.instructions == opmul_instr
        assert compiler.current_scope.last_instruction == EmittedInstruction(opcodes.OPMUL, 0)

        compiler.emit(opcodes.OPSUB)

        assert compiler.number_of_scopes == 1
        assert compiler.current_scope.instructions == opmulsub_instr
        assert compiler.current_scope.second_last_instruction == EmittedInstruction(opcodes.OPMUL, 0)
        assert compiler.current_scope.last_instruction == EmittedInstruction(opcodes.OPSUB, 1)

    def test_enter_scope_symbol_table(self) -> None:
        compiler = Compiler()

        current_symbol_table = compiler.symbol_table
        assert current_symbol_table.outer_table is None

        compiler.enter_scope()

        assert current_symbol_table is not compiler.symbol_table
        assert current_symbol_table is compiler.symbol_table.outer_table

    def test_enter_scope_and_leave_scope_symbol_table(self) -> None:
        compiler = Compiler()

        current_symbol_table = compiler.symbol_table
        assert current_symbol_table.outer_table is None

        compiler.enter_scope()
        compiler.leave_scope()

        assert current_symbol_table is compiler.symbol_table


class TestCompilationScope:
    def test_default_construction(self) -> None:
        default_scope = CompilationScope()

        assert default_scope.instructions == Instructions()
        assert default_scope.last_instruction == EmittedInstruction()
        assert default_scope.second_last_instruction == EmittedInstruction()
