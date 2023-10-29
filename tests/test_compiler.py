import pytest

from monkey.compiler import Compiler
from monkey.compiler import compile
from monkey.compiler import bytecode_from_compiler

import monkey.code.opcodes as op

from compiler_utils import parse
from compiler_utils import CompilerInfixTestCase
from compiler_utils import CompilerBooleanTestCase


class TestCompiler:
    @pytest.mark.parametrize(
        "case",
        [
            CompilerInfixTestCase(
                "1;",
                (1,),
                [(op.OPCONSTANT, (0,)), (op.OPPOP, ())],
            ),
            CompilerInfixTestCase(
                "1 + 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPADD, ()), (op.OPPOP, ())],
            ),
            CompilerInfixTestCase(
                "1 - 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPSUB, ()), (op.OPPOP, ())],
            ),
            CompilerInfixTestCase(
                "1 * 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPMUL, ()), (op.OPPOP, ())],
            ),
            CompilerInfixTestCase(
                "2 / 1;",
                (2, 1),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPDIV, ()), (op.OPPOP, ())],
            ),
            CompilerInfixTestCase(
                "1 > 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPGREATERTHAN, ()), (op.OPPOP, ())],
            ),
            CompilerInfixTestCase(
                "1 != 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPNOTEQUAL, ()), (op.OPPOP, ())],
            ),
            CompilerInfixTestCase(
                "1 == 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPEQUAL, ()), (op.OPPOP, ())],
            ),
            CompilerInfixTestCase(
                "1 < 2;",
                (2, 1),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPGREATERTHAN, ()), (op.OPPOP, ())],
            ),
            CompilerInfixTestCase(
                "true == false;",
                (),
                [(op.OPTRUE, ()), (op.OPFALSE, ()), (op.OPEQUAL, ()), (op.OPPOP, ())],
            ),
            CompilerInfixTestCase(
                "false == true;",
                (),
                [(op.OPFALSE, ()), (op.OPTRUE, ()), (op.OPEQUAL, ()), (op.OPPOP, ())],
            ),
            CompilerInfixTestCase(
                "true != false;",
                (),
                [(op.OPTRUE, ()), (op.OPFALSE, ()), (op.OPNOTEQUAL, ()), (op.OPPOP, ())],
            ),
        ],
    )
    def test_infix_case(self, case: CompilerInfixTestCase):
        program = parse(case.input_text)
        compiler = Compiler()

        compile(compiler, program)
        bytecode = bytecode_from_compiler(compiler)

        assert bytecode.instructions == case.instructions
        assert bytecode.constants == case.constants

    @pytest.mark.parametrize(
        "case",
        [
            CompilerBooleanTestCase(
                "true;",
                [(op.OPTRUE, ()), (op.OPPOP, ())],
            ),
            CompilerBooleanTestCase(
                "false;",
                [(op.OPFALSE, ()), (op.OPPOP, ())],
            ),
        ],
    )
    def test_boolean_literal(self, case: CompilerBooleanTestCase):
        program = parse(case.input_text)
        compiler = Compiler()

        compile(compiler, program)
        bytecode = bytecode_from_compiler(compiler)

        assert bytecode.instructions == case.instructions
        assert len(bytecode.constants) == 0
