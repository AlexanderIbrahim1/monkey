import pytest

from monkey.code.opcodes import OPADD
from monkey.code.opcodes import OPCONSTANT
from monkey.code.opcodes import OPPOP
from monkey.compiler import Compiler
from monkey.compiler import compile
from monkey.compiler import bytecode_from_compiler
from monkey.code import instructions_to_string

from compiler_utils import parse
from compiler_utils import CompilerArithmeticTestCase


class TestCompiler:
    @pytest.mark.parametrize(
        "case",
        [
            CompilerArithmeticTestCase(
                "1 + 2;", (1, 2), [(OPCONSTANT, (0,)), (OPCONSTANT, (1,)), (OPADD, ()), (OPPOP, ())]
            ),
            # CompilerArithmeticTestCase(
            #     "1 - 2;", (1, 2), [(OPCONSTANT, (0,)), (OPCONSTANT, (1,)), (OPPOP, ())]
            # ),
        ],
    )
    def test_integer_arithmetic(self, case: CompilerArithmeticTestCase):
        program = parse(case.input_text)
        compiler = Compiler()

        compile(compiler, program)
        bytecode = bytecode_from_compiler(compiler)

        print(instructions_to_string(bytecode.instructions))
        print(instructions_to_string(case.instructions))

        assert bytecode.instructions == case.instructions
        assert bytecode.constants == case.constants
