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
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                (op.OPCONSTANT, (0,)),
                                (op.OPCONSTANT, (1,)),
                                (op.OPADD, ()),
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        0,
                    ),
                ),
                [
                    # the compiled function is a constant, so we can push it on the stack as one
                    (op.OPCONSTANT, (2,)),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
            # identical to the above case, but now for an implicit return
            CompilerTestCase(
                "fn() { 5 + 10 };",
                (
                    5,
                    10,
                    # the argument to the compiled function is the bytecode for the operations that
                    # take place in its body
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                (op.OPCONSTANT, (0,)),
                                (op.OPCONSTANT, (1,)),
                                (op.OPADD, ()),
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        0,
                    ),
                ),
                [
                    # the compiled function is a constant, so we can push it on the stack as one
                    (op.OPCONSTANT, (2,)),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                "fn() { 1; 2 };",
                (
                    1,
                    2,
                    # the argument to the compiled function is the bytecode for the operations that
                    # take place in its body
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                (op.OPCONSTANT, (0,)),
                                (op.OPPOP, ()),
                                (op.OPCONSTANT, (1,)),
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        0,
                    ),
                ),
                [
                    # the compiled function is a constant, so we can push it on the stack as one
                    (op.OPCONSTANT, (2,)),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                "fn() {};",
                (
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                (op.OPRETURN, ()),
                            ]
                        ),
                        0,
                    ),
                ),
                [
                    # the compiled function is a constant, so we can push it on the stack as one
                    (op.OPCONSTANT, (0,)),
                    # we have an expression statement; need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_compiled_function(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                "fn() { 24 }();",
                (
                    24,
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                (op.OPCONSTANT, (0,)),
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        0,
                    ),
                ),
                [
                    # the compiled function is a constant, so we can push it on the stack as one
                    (op.OPCONSTANT, (1,)),
                    # we are calling the function on top of the stack
                    (op.OPCALL, ()),
                    # we have an expression statement; we need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                "let my_func = fn() { 24 }; my_func();",
                (
                    24,
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                (op.OPCONSTANT, (0,)),
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        0,
                    ),
                ),
                [
                    # the compiled function is a constant, so we can push it on the stack as one
                    (op.OPCONSTANT, (1,)),
                    # bind variable '0' to the object on top of the stack (the compiled function)
                    (op.OPSETGLOBAL, (0,)),
                    # retrieve the variable referred to by '0' (the compiled function)
                    (op.OPGETGLOBAL, (0,)),
                    # we are calling the function on top of the stack
                    (op.OPCALL, ()),
                    # we have an expression statement; we need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_function_call(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                """
                let outer = fn() {
                    let inner = fn() { return 1; };
                    return inner;
                };
                let f = outer();
                f();
                """,
                (
                    1,
                    # bytecode instructions for the body of the `inner` function
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # we create the constant `1`, and put it on the stack
                                # it is the first constant, so we assign it label 0
                                (op.OPCONSTANT, (0,)),
                                # we do nothing but return the thing on top of the stack (constant label 0)
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        0,
                    ),
                    # bytecode instructions for the body of the `outer` function
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the `inner` function is a constant; we put it on top of the stack
                                # it is the second constant, so we assign it label 1
                                (op.OPCONSTANT, (1,)),
                                # we bind the variable name `inner`
                                # it is the first binding, so we assign it a label of `0`
                                # the VM will map the index `0` in the bindings list, to the index `1` of the constants
                                (op.OPSETLOCAL, (0,)),
                                # we are about to return `inner`, and to do this, we need to refer to it
                                # put `inner` on top of the stack, with OPSETGLOBAL
                                (op.OPGETLOCAL, (0,)),
                                # we want the thing we just put on top of the stack to remain there
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        1,
                    ),
                ),
                [
                    # push the `outer` function as a constant to the stack
                    (op.OPCONSTANT, (2,)),
                    # `outer` is the first variable to be bound globally; set it to 0
                    # it gets popped off the stack, and into the globals
                    (op.OPSETGLOBAL, (0,)),
                    # we are looking up the `outer` function (remember it was set to `0`)
                    # this OPGETGLOBAL puts it on top of the stack
                    (op.OPGETGLOBAL, (0,)),
                    # we are calling the `outer` function (remember it is on top of the stack, at `2`)
                    (op.OPCALL, ()),
                    # `f` is the third variable to be bound; set it to label `2`
                    (op.OPSETGLOBAL, (1,)),
                    # on the very next line, we refer to variable `f` (remember it was set to label `2`)
                    (op.OPGETGLOBAL, (1,)),
                    # OPGETGLOBAL puts whatever we just asked from, from the constants, on top of the stack
                    # so now we can call the thing on top of the stack
                    (op.OPCALL, ()),
                    # the last line `f();` is an expression statement; we want it off the stack now
                    (op.OPPOP, ()),
                ],
            )
        ],
    )
    def test_first_class_function_call(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                """
                let outer = fn() {
                    let inner = fn() { return 1; };
                    return inner;
                };
                outer()();
                """,
                (
                    1,
                    # bytecode instructions for the body of the `inner` function
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # we create the constant `1`, and put it on the stack
                                # it is the first constant, so we assign it label 0
                                (op.OPCONSTANT, (0,)),
                                # we do nothing but return the thing on top of the stack (constant label 0)
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        0,
                    ),
                    # bytecode instructions for the body of the `outer` function
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the `inner` function is a constant; we put it on top of the stack
                                # it is the second constant, so we assign it label 1
                                (op.OPCONSTANT, (1,)),
                                # we bind the variable name `inner`
                                # it is the first binding, so we assign it a label of `0`
                                # the VM will map the index `0` in the bindings list, to the index `1` of the constants
                                (op.OPSETLOCAL, (0,)),
                                # we are about to return `inner`, and to do this, we need to refer to it
                                # put `inner` on top of the stack, with OPSETGLOBAL
                                (op.OPGETLOCAL, (0,)),
                                # we want the thing we just put on top of the stack to remain there
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        1,
                    ),
                ),
                [
                    # push the `outer` function as a constant to the stack
                    (op.OPCONSTANT, (2,)),
                    # `outer` is the first variable to be bound globally; set it to 0
                    # it gets popped off the stack, and into the globals
                    (op.OPSETGLOBAL, (0,)),
                    # we are looking up the `outer` function (remember it was set to `0`)
                    # this OPGETGLOBAL puts it on top of the stack
                    (op.OPGETGLOBAL, (0,)),
                    # we are calling the `outer` function (remember, it is now on top of the stack)
                    (op.OPCALL, ()),
                    # we (again) call the thing on top of the stack; this is whatever `outer()` returned
                    (op.OPCALL, ()),
                    # the last line `f();` is an expression statement; we want it off the stack now
                    (op.OPPOP, ()),
                ],
            )
        ],
    )
    def test_first_class_function_call_direct(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                """
                let num = 55;
                fn() { num };
                """,
                (
                    55,
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                (op.OPGETGLOBAL, (0,)),
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        0,
                    ),
                ),
                [
                    # look for the constant '55' in the 'constants'; push it onto the stack
                    # it is the first constant, so it is labelled 0
                    (op.OPCONSTANT, (0,)),
                    # take the thing on top of the stack (number '55'), pop it off the stack, then
                    # bind it to a global name 'num'; it is the first global name, so it is labelled 0
                    (op.OPSETGLOBAL, (0,)),
                    # look for the constant function in the 'constants'; put it onto the stack
                    # the function is the second global name, so it is labelled 1
                    (op.OPCONSTANT, (1,)),
                    # this is an expression statement; we don't want it to linger on the stack
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                """
                fn() {
                    let num = 55;
                    return num;
                };
                """,
                (
                    55,
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the number '55' is the first constant; find it in the 'constants', and
                                # put it on top of the stack
                                (op.OPCONSTANT, (0,)),
                                # take the thing on top of the stack (the number '55'), pop it off, bind it to
                                # a name, and put it in the binding stack;
                                # it is the first bound name, so it is labelled 0
                                (op.OPSETLOCAL, (0,)),
                                # look for the symbol in the binding stack that corresponds to 0; push it on top
                                # of the stack
                                (op.OPGETLOCAL, (0,)),
                                # we want the thing we just put on top of the stack to remain there
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        1,
                    ),
                ),
                [
                    # the function itself is a constant; look for it in the 'constants', and push it
                    # on top of the stack
                    (op.OPCONSTANT, (1,)),
                    # this is an expression statement; we don't want it to linger on the stack
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_let_statement_scopes(self, case: CompilerTestCase):
        perform_compiler_test_case(case)


# NOTE TO DEV: the number of locals in a function is the unique number of variables
# that are defined in the function's body; not every constant gets a binding, so the
# constants that are just expression statements on their own do not count towards
# the number of local bindings
