import pytest

from monkey.compiler import Compiler
from monkey.compiler import compile
from monkey.compiler import EmittedInstruction

import monkey.code as code
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

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                "[];",
                (),
                [
                    # an OPARRAY to indicate that there's an array, and the number of elements
                    (op.OPARRAY, (0,)),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                "[1, 2, 3];",
                (1, 2, 3),
                [
                    # there are three constant literals we can push onto the stack
                    (op.OPCONSTANT, (0,)),
                    (op.OPCONSTANT, (1,)),
                    (op.OPCONSTANT, (2,)),
                    # an OPARRAY to indicate that there's an array, and the number of elements
                    (op.OPARRAY, (3,)),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                "[1 + 2, 3 - 4, 5 * 6];",
                (1, 2, 3, 4, 5, 6),
                [
                    # the first element is made by pushing constants 1 and 2, and adding them
                    (op.OPCONSTANT, (0,)),
                    (op.OPCONSTANT, (1,)),
                    (op.OPADD, ()),
                    # the second element is made by pushing constants 3 and 4, with a subtraction
                    (op.OPCONSTANT, (2,)),
                    (op.OPCONSTANT, (3,)),
                    (op.OPSUB, ()),
                    # the third element is made by pushing constants 3 and 4, with a multiplication
                    (op.OPCONSTANT, (4,)),
                    (op.OPCONSTANT, (5,)),
                    (op.OPMUL, ()),
                    # an OPARRAY to indicate that there's an array, and the number of elements
                    # notice that even though there are 6 things on the stack, there are still
                    # only 3 elements
                    (op.OPARRAY, (3,)),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_array_literal(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                "{};",
                (),
                [
                    # an OPHASH to indicate that there's a hash, 0 = number of keys and values together
                    (op.OPHASH, (0,)),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                "{1: 2, 3: 4, 5: 6};",
                (1, 2, 3, 4, 5, 6),
                [
                    # there are six constant literals we can push onto the stack
                    (op.OPCONSTANT, (0,)),
                    (op.OPCONSTANT, (1,)),
                    (op.OPCONSTANT, (2,)),
                    (op.OPCONSTANT, (3,)),
                    (op.OPCONSTANT, (4,)),
                    (op.OPCONSTANT, (5,)),
                    # an OPHASH to indicate that there's a hash, 6 = number of keys and values together
                    (op.OPHASH, (6,)),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                "{1: 2 + 3, 4: 5 * 6};",
                (1, 2, 3, 4, 5, 6),
                [
                    # the first element (1) is pushed on, and that's it
                    (op.OPCONSTANT, (0,)),
                    # the next two elements (2, 3) are pushed on, then added
                    (op.OPCONSTANT, (1,)),
                    (op.OPCONSTANT, (2,)),
                    (op.OPADD, ()),
                    # the fourth element (4) is pushed on, and that's it
                    (op.OPCONSTANT, (3,)),
                    # the next two elements (5, 6) are pushed on, then multiplied
                    (op.OPCONSTANT, (4,)),
                    (op.OPCONSTANT, (5,)),
                    (op.OPMUL, ()),
                    # an OPHASH to indicate that there's a hash, 4 = number of keys and values together
                    (op.OPHASH, (4,)),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_hash_literal(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                "[1, 2, 3][1 + 1];",
                (1, 2, 3, 1, 1),
                [
                    # the array begins by pushing all its constants
                    (op.OPCONSTANT, (0,)),
                    (op.OPCONSTANT, (1,)),
                    (op.OPCONSTANT, (2,)),
                    # an OPARRAY to indicate that there's an array, and the number of elements
                    (op.OPARRAY, (3,)),
                    # the index is created by pushing all its constants, then adding them
                    (op.OPCONSTANT, (3,)),
                    (op.OPCONSTANT, (4,)),
                    (op.OPADD, ()),
                    # now perform the indexing expression
                    (op.OPINDEX, ()),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_array_index_expressions(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                "{1: 2, 3: 4}[3];",
                (1, 2, 3, 4, 3),
                [
                    # the hash begins by pushing all its constants
                    (op.OPCONSTANT, (0,)),
                    (op.OPCONSTANT, (1,)),
                    (op.OPCONSTANT, (2,)),
                    (op.OPCONSTANT, (3,)),
                    # an OPHASH to indicate that there's a hash, and the total number of objects
                    (op.OPHASH, (4,)),
                    # the index is created by pushing it as a constant
                    (op.OPCONSTANT, (4,)),
                    # now perform the indexing expression
                    (op.OPINDEX, ()),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_hash_index_expressions(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                "fn() { return 5 + 10; };",
                (
                    5,
                    10,
                    # the argument to the compiled function is the bytecode for the operations that
                    # take place in its body
                    code.make_instructions_from_opcode_operand_pairs(
                        [
                            (op.OPCONSTANT, (0,)),
                            (op.OPCONSTANT, (1,)),
                            (op.OPADD, ()),
                            (op.OPRETURNVALUE, ()),
                        ]
                    ),
                ),
                [
                    # the compiled function is a constant, so we can push it on the stack as one
                    (op.OPCONSTANT, (2,)),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
            #            # identical to the above case, but now for an implicit return
            #            CompilerTestCase(
            #                "fn() { 5 + 10 };",
            #                (
            #                    5,
            #                    10,
            #                    # the argument to the compiled function is the bytecode for the operations that
            #                    # take place in its body
            #                    code.make_instructions_from_opcode_operand_pairs(
            #                        [
            #                            (op.OPCONSTANT, (0,)),
            #                            (op.OPCONSTANT, (1,)),
            #                            (op.OPADD, ()),
            #                            (op.OPRETURNVALUE, ()),
            #                        ]
            #                    ),
            #                ),
            #                [
            #                    # the compiled function is a constant, so we can push it on the stack as one
            #                    (op.OPCONSTANT, (2,)),
            #                    # we have an expression statement; need to pop it off
            #                    (op.OPPOP, ()),
            #                ],
            #            ),
        ],
    )
    def test_compiled_function(self, case: CompilerTestCase):
        perform_compiler_test_case(case)
