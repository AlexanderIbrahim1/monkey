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


class TestCompilationScope:
    def test_default_construction(self) -> None:
        default_scope = CompilationScope()

        assert default_scope.instructions == Instructions()
        assert default_scope.last_instruction == EmittedInstruction()
        assert default_scope.second_last_instruction == EmittedInstruction()
