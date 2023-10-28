import pytest

from monkey.compiler import Compiler
from monkey.compiler import compile
from monkey.compiler import bytecode_from_compiler
from monkey.code import instructions_to_string

import monkey.code.opcodes as op

from compiler_utils import parse
from compiler_utils import CompilerArithmeticTestCase


class TestCompiler:
    @pytest.mark.parametrize(
        "case",
        [
            CompilerArithmeticTestCase(
                "1 + 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPADD, ()), (op.OPPOP, ())],
            ),
            CompilerArithmeticTestCase(
                "1 - 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPSUB, ()), (op.OPPOP, ())],
            ),
            CompilerArithmeticTestCase(
                "1 * 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPMUL, ()), (op.OPPOP, ())],
            ),
            CompilerArithmeticTestCase(
                "2 / 1;",
                (2, 1),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPDIV, ()), (op.OPPOP, ())],
            ),
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
