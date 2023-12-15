from monkey.code.code import Instructions

from monkey.compiler.compilation_scope import CompilationScope
from monkey.compiler.emitted_instruction import EmittedInstruction


class TestCompilationScope:
    def test_default_construction(self) -> None:
        default_scope = CompilationScope()

        assert default_scope.instructions == Instructions()
        assert default_scope.last_instruction == EmittedInstruction()
        assert default_scope.second_last_instruction == EmittedInstruction()
