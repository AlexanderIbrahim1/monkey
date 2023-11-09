import pytest

from monkey.compiler import Compiler
from monkey.compiler import compile
from monkey.compiler import EmittedInstruction

import monkey.code.opcodes as op

from compiler_utils import CompilerTestCase
from compiler_utils import parse
from compiler_utils import perform_compiler_test_case


class TestCompiler:
    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                "1;",
                (1,),
                [(op.OPCONSTANT, (0,)), (op.OPPOP, ())],
            ),
            CompilerTestCase(
                "true;",
                (),
                [(op.OPTRUE, ()), (op.OPPOP, ())],
            ),
            CompilerTestCase(
                "false;",
                (),
                [(op.OPFALSE, ()), (op.OPPOP, ())],
            ),
        ],
    )
    def test_op_constant(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                "1 + 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPADD, ()), (op.OPPOP, ())],
            ),
            CompilerTestCase(
                "1 - 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPSUB, ()), (op.OPPOP, ())],
            ),
            CompilerTestCase(
                "1 * 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPMUL, ()), (op.OPPOP, ())],
            ),
            CompilerTestCase(
                "2 / 1;",
                (2, 1),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPDIV, ()), (op.OPPOP, ())],
            ),
            CompilerTestCase(
                "1 > 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPGREATERTHAN, ()), (op.OPPOP, ())],
            ),
            CompilerTestCase(
                "1 != 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPNOTEQUAL, ()), (op.OPPOP, ())],
            ),
            CompilerTestCase(
                "1 == 2;",
                (1, 2),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPEQUAL, ()), (op.OPPOP, ())],
            ),
            CompilerTestCase(
                "1 < 2;",
                (2, 1),
                [(op.OPCONSTANT, (0,)), (op.OPCONSTANT, (1,)), (op.OPGREATERTHAN, ()), (op.OPPOP, ())],
            ),
            CompilerTestCase(
                "true == false;",
                (),
                [(op.OPTRUE, ()), (op.OPFALSE, ()), (op.OPEQUAL, ()), (op.OPPOP, ())],
            ),
            CompilerTestCase(
                "false == true;",
                (),
                [(op.OPFALSE, ()), (op.OPTRUE, ()), (op.OPEQUAL, ()), (op.OPPOP, ())],
            ),
            CompilerTestCase(
                "true != false;",
                (),
                [(op.OPTRUE, ()), (op.OPFALSE, ()), (op.OPNOTEQUAL, ()), (op.OPPOP, ())],
            ),
        ],
    )
    def test_infix_operator(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                "-1;",
                (1,),
                [(op.OPCONSTANT, (0,)), (op.OPMINUS, ()), (op.OPPOP, ())],
            ),
            CompilerTestCase(
                "!true;",
                (),
                [(op.OPTRUE, ()), (op.OPBANG, ()), (op.OPPOP, ())],
            ),
        ],
    )
    def test_prefix_operator(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                "if (true) { 10 }; 3333;",
                (10, 3333),
                [
                    # 0000 [the condition]
                    (op.OPTRUE, ()),
                    # 0001 [skip to the NULL if false]
                    (op.OPJUMPWHENFALSE, (10,)),
                    # 0004 [holds the 10]
                    (op.OPCONSTANT, (0,)),
                    # 0007 [jump over the NULL]
                    (op.OPJUMP, (11,)),
                    # 0010 [the instruction found if there is no alternative, and condition is false]
                    (op.OPNULL, ()),
                    # 0011 [pop the 10 or the NULL]
                    (op.OPPOP, ()),
                    # 0012 [holds the 3333]
                    (op.OPCONSTANT, (1,)),
                    # 0015 [pop the 3333]
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                "if (true) { 10 } else { 20 }; 3333;",
                (10, 20, 3333),
                [
                    # 0000 [the condition]
                    (op.OPTRUE, ()),
                    # 0001 [skip to the location of the 20 if false; else, keep going]
                    (op.OPJUMPWHENFALSE, (10,)),
                    # 0004 [holds the 10]
                    (op.OPCONSTANT, (0,)),
                    # 0007 [skip past the 20, because 10 has already been loaded]
                    (op.OPJUMP, (13,)),
                    # 0010 [holds the 20]
                    (op.OPCONSTANT, (1,)),
                    # 0013 [pop the 10 or 20, whichever is there]
                    (op.OPPOP, ()),
                    # 0008 [holds the 3333]
                    (op.OPCONSTANT, (2,)),
                    # 0011 [pop the 3333]
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_if_else_expressions(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    def test_emitted_instructions(self):
        input_text = "1;"
        program = parse(input_text)
        compiler = Compiler()

        compile(compiler, program)

        # 0000 -> OPCONSTANT
        # 0001 -> first byte of the constant
        # 0002 -> second byte of the constant
        # 0003 -> OPPOP
        expected_last_instruction = EmittedInstruction(op.OPPOP, 3)
        expected_second_last_instruction = EmittedInstruction(op.OPCONSTANT, 0)

        assert compiler.last_instruction == expected_last_instruction
        assert compiler.second_last_instruction == expected_second_last_instruction

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                "let one = 1; let two = 2;",
                (1, 2),
                [
                    # push '1' onto the stack
                    (op.OPCONSTANT, (0,)),
                    # bind value '1' to variable 'one' (labelled 0)
                    (op.OPSETGLOBAL, (0,)),
                    # push '2' onto the stack
                    (op.OPCONSTANT, (1,)),
                    # bind value '2' to variable 'two' (labelled 1)
                    (op.OPSETGLOBAL, (1,)),
                ],
            ),
            CompilerTestCase(
                "let one = 1; one;",
                (1,),
                [
                    # push '1' onto the stack
                    (op.OPCONSTANT, (0,)),
                    # bind value '1' to variable 'one' (labelled 0)
                    (op.OPSETGLOBAL, (0,)),
                    # retrieve the value bound to variable 'one' (labelled 0), put on top of stack
                    (op.OPGETGLOBAL, (0,)),
                    # 'one;' is an expression statement; pop its value off the stack
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                "let one = 1; let two = one; two;",
                (1,),
                [
                    # push '1' onto the stack
                    (op.OPCONSTANT, (0,)),
                    # bind value '1' to variable 'one' (labelled 0)
                    (op.OPSETGLOBAL, (0,)),
                    # retrieve the value bound to variable 'one' (labelled 0), put on top of stack
                    (op.OPGETGLOBAL, (0,)),
                    # bind value '1' (from 'one') to variable 'two' (labelled 1)
                    (op.OPSETGLOBAL, (1,)),
                    # retrieve the value bound to variable 'two' (labelled 1), put on top of stack
                    (op.OPGETGLOBAL, (1,)),
                    # 'two;' is an expression statement; pop its value off the stack
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_global_let_statement(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                '"monkey";',
                ("monkey",),
                [
                    # string literals are treated as constants; push them on the stack, like ints
                    (op.OPCONSTANT, (0,)),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                '"mon" + "key";',
                ("mon", "key"),
                [
                    # just like for integers, push both "mon" and "key" onto the stack
                    (op.OPCONSTANT, (0,)),
                    (op.OPCONSTANT, (1,)),
                    # just like for integers, OPADD adds the two topmost things on the stack
                    (op.OPADD, ()),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_string_literals(self, case: CompilerTestCase):
        perform_compiler_test_case(case)
