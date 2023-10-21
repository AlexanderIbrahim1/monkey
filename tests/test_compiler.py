import pytest

from monkey.code.opcodes import OPCONSTANT
from monkey.compiler import Compiler
from monkey.compiler import compile
from monkey.compiler import bytecode_from_compiler

from compiler_utils import parse
from compiler_utils import CompilerArithmeticTestCase


class TestCompiler:
    @pytest.mark.parametrize(
        "case",
        [
            CompilerArithmeticTestCase("1 + 2;", (1, 2), [(OPCONSTANT, (0,)), (OPCONSTANT, (1,))]),
            CompilerArithmeticTestCase("1 - 2;", (1, 2), [(OPCONSTANT, (0,)), (OPCONSTANT, (1,))]),
        ],
    )
    def test_integer_arithmetic(self, case: CompilerArithmeticTestCase):
        program = parse(case.input_text)
        compiler = Compiler()

        compile(compiler, program)
        bytecode = bytecode_from_compiler(compiler)

        assert bytecode.instructions == case.instructions
        assert bytecode.constants == case.constants
