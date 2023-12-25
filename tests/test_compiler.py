import pytest

from monkey.compiler import Compiler
from monkey.compiler import compile
from monkey.compiler import EmittedInstruction

import monkey.object.monkey_builtins as monkey_builtins
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
                        # no local bindings
                        0,
                        # no arguments
                        0,
                    ),
                ),
                [
                    # the compiled function is a constant, so we can push it on the stack as one
                    (op.OPCLOSURE, (2, 0)),
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
                        # no local bindings
                        0,
                        # no arguments
                        0,
                    ),
                ),
                [
                    # the compiled function is a constant, so we can push it on the stack as one
                    (op.OPCLOSURE, (2, 0)),
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
                        # no local bindings
                        0,
                        # no arguments
                        0,
                    ),
                ),
                [
                    # the compiled function is a constant, so we can push it on the stack as one
                    (op.OPCLOSURE, (2, 0)),
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
                        # no local bindings
                        0,
                        # no arguments
                        0,
                    ),
                ),
                [
                    # the compiled function is a constant, so we can push it on the stack as one
                    (op.OPCLOSURE, (0, 0)),
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
                        # no local bindings
                        0,
                        # no arguments
                        0,
                    ),
                ),
                [
                    # the compiled function is a constant, so we can push it on the stack as one
                    (op.OPCLOSURE, (1, 0)),
                    # we are calling the function on top of the stack
                    (op.OPCALL, (0,)),
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
                        # no local bindings
                        0,
                        # no arguments
                        0,
                    ),
                ),
                [
                    # the compiled function is a constant, so we can push it on the stack as one
                    (op.OPCLOSURE, (1, 0)),
                    # bind variable '0' to the object on top of the stack (the compiled function)
                    (op.OPSETGLOBAL, (0,)),
                    # retrieve the variable referred to by '0' (the compiled function)
                    (op.OPGETGLOBAL, (0,)),
                    # we are calling the function on top of the stack
                    (op.OPCALL, (0,)),
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
                        # no local bindings
                        0,
                        # no arguments
                        0,
                    ),
                    # bytecode instructions for the body of the `outer` function
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the `inner` function is a constant; we put it on top of the stack
                                # it is the second constant, so we assign it label 1
                                (op.OPCLOSURE, (1, 0)),
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
                        # no local bindings
                        1,
                        # no arguments
                        0,
                    ),
                ),
                [
                    # push the `outer` function as a constant to the stack
                    (op.OPCLOSURE, (2, 0)),
                    # `outer` is the first variable to be bound globally; set it to 0
                    # it gets popped off the stack, and into the globals
                    (op.OPSETGLOBAL, (0,)),
                    # we are looking up the `outer` function (remember it was set to `0`)
                    # this OPGETGLOBAL puts it on top of the stack
                    (op.OPGETGLOBAL, (0,)),
                    # we are calling the `outer` function (remember it is on top of the stack, at `2`)
                    (op.OPCALL, (0,)),
                    # `f` is the third variable to be bound; set it to label `2`
                    (op.OPSETGLOBAL, (1,)),
                    # on the very next line, we refer to variable `f` (remember it was set to label `2`)
                    (op.OPGETGLOBAL, (1,)),
                    # OPGETGLOBAL puts whatever we just asked from, from the constants, on top of the stack
                    # so now we can call the thing on top of the stack
                    (op.OPCALL, (0,)),
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
                        # no local bindings
                        0,
                        # no arguments
                        0,
                    ),
                    # bytecode instructions for the body of the `outer` function
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the `inner` function is a constant; we put it on top of the stack
                                # it is the second constant, so we assign it label 1
                                (op.OPCLOSURE, (1, 0)),
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
                        # one local binding (`inner`)
                        1,
                        # no arguments
                        0,
                    ),
                ),
                [
                    # push the `outer` function as a constant to the stack
                    (op.OPCLOSURE, (2, 0)),
                    # `outer` is the first variable to be bound globally; set it to 0
                    # it gets popped off the stack, and into the globals
                    (op.OPSETGLOBAL, (0,)),
                    # we are looking up the `outer` function (remember it was set to `0`)
                    # this OPGETGLOBAL puts it on top of the stack
                    (op.OPGETGLOBAL, (0,)),
                    # we are calling the `outer` function (remember, it is now on top of the stack)
                    (op.OPCALL, (0,)),
                    # we (again) call the thing on top of the stack; this is whatever `outer()` returned
                    (op.OPCALL, (0,)),
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
                        # no local bindings
                        0,
                        # no arguments
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
                    (op.OPCLOSURE, (1, 0)),
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
                        # one local binding (`num`)
                        1,
                        # no arguments
                        0,
                    ),
                ),
                [
                    # the function itself is a constant; look for it in the 'constants', and push it
                    # on top of the stack
                    (op.OPCLOSURE, (1, 0)),
                    # this is an expression statement; we don't want it to linger on the stack
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_let_statement_scopes(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                """
                fn(a) {};
                """,
                (
                    (
                        # bytecode instructions for the body of the function
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the function body is empty; all it does is go back to where we left off
                                # i.e. OPRETURN tells it to pop the function body off the stack, and push a NULL
                                (op.OPRETURN, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # one argument
                        1,
                    ),
                ),
                [
                    # the function itself is a contant; it is the first, so label it as 0
                    (op.OPCLOSURE, (0, 0)),
                    # we have an expression statement, so we need to pop it off the stack
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                """
                let one_arg = fn(a) {};
                """,
                (
                    (
                        # bytecode instructions for the body of the function
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the function body is empty; all it does is go back to where we left off
                                # i.e. OPRETURN pops the function body off the stack, and pushes a NULL
                                (op.OPRETURN, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # one argument
                        1,
                    ),
                ),
                [
                    # the function itself is a constant; it is the first, so label it as 0
                    (op.OPCLOSURE, (0, 0)),
                    # we create a global binding for the name `one_arg` (pop off stack, put in globals)
                    (op.OPSETGLOBAL, (0,)),
                    # note that a let statement is not an expression statement; we don't pop the thing
                    # off the top of the stack right away
                ],
            ),
            CompilerTestCase(
                """
                let one_arg = fn(a) {};
                one_arg(25);
                """,
                (
                    # the first constant is the function
                    (
                        # bytecode instructions for the body of the function
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the function body is empty; all it does is go back to where we left off
                                # i.e. OPRETURN pops the function body off the stack, and pushes a NULL
                                (op.OPRETURN, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # one argument
                        1,
                    ),
                    # the next constant is the 25 that gets passed as an argument
                    25,
                ),
                [
                    # the function itself is a constant; it is the first, so label it as 0
                    (op.OPCLOSURE, (0, 0)),
                    # we create a global binding for the name `one_arg` (pop off stack, put in globals)
                    # note that a let statement is not an expression statement; we don't pop the thing
                    # off the top of the stack right away
                    (op.OPSETGLOBAL, (0,)),
                    # we are referencing a name `one_arg`, so search for it in the globals, and push it
                    # on top of the stack; the function was labelled as 0
                    (op.OPGETGLOBAL, (0,)),
                    # the function takes one argument
                    # the argument is a constant, so we deal with it using OPCONSTANT
                    (op.OPCONSTANT, (1,)),
                    # with the function and its arguments on the stack, we call!
                    (op.OPCALL, (1,)),
                    # the line with the call is an expression statement; we pop it off the stack
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                """
                let three_args = fn(a, b, c) {};
                three_args(24, 25, 26);
                """,
                (
                    # the first constant is the function
                    (
                        # bytecode instructions for the body of the function
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the function body is empty; all it does is go back to where we left off
                                # i.e. OPRETURN pops the function body off the stack, and pushes a NULL
                                (op.OPRETURN, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # three arguments
                        3,
                    ),
                    # the next constants are the 24, 25, 26 that get passed as arguments
                    24,
                    25,
                    26,
                ),
                [
                    # the function itself is a constant; it is the first, so label it as 0
                    (op.OPCLOSURE, (0, 0)),
                    # we create a global binding for the name `three_args` (pop off stack, put in globals)
                    # note that a let statement is not an expression statement; we don't pop the thing
                    # off the top of the stack right away
                    (op.OPSETGLOBAL, (0,)),
                    # we are referencing a name `three_args`, so search for it in the globals, and push it
                    # on top of the stack; the function was labelled as 0
                    (op.OPGETGLOBAL, (0,)),
                    # the function takes three arguments
                    # all three arguments are constants, so we put them in the constants
                    (op.OPCONSTANT, (1,)),
                    (op.OPCONSTANT, (2,)),
                    (op.OPCONSTANT, (3,)),
                    # with the function and its arguments on the stack, we call!
                    (op.OPCALL, (3,)),
                    # the line with the call is an expression statement; we pop it off the stack
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_function_call_with_arguments_no_body(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                """
                let global_num = 10;
                let sum_with_global_twice = fn(a) {
                    return a + global_num + global_num;
                };
                sum_with_global_twice(5);
                """,
                (
                    10,
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                (op.OPGETLOCAL, (0,)),
                                (op.OPGETGLOBAL, (0,)),
                                (op.OPADD, ()),
                                (op.OPGETGLOBAL, (0,)),
                                (op.OPADD, ()),
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # one argument (`a`)
                        1,
                    ),
                    5,
                ),
                [
                    (op.OPCONSTANT, (0,)),
                    (op.OPSETGLOBAL, (0,)),
                    (op.OPCLOSURE, (1, 0)),
                    (op.OPSETGLOBAL, (1,)),
                    (op.OPGETGLOBAL, (1,)),
                    (op.OPCONSTANT, (2,)),
                    (op.OPCALL, (1,)),
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                """
                let global_num = 10;
                let sum_with_global = fn(a) {
                    return a + global_num;
                };
                sum_with_global(1) + sum_with_global(2);
                """,
                (
                    10,
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                (op.OPGETLOCAL, (0,)),
                                (op.OPGETGLOBAL, (0,)),
                                (op.OPADD, ()),
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # one argument (`a`)
                        1,
                    ),
                    1,
                    2,
                ),
                [
                    (op.OPCONSTANT, (0,)),
                    (op.OPSETGLOBAL, (0,)),
                    (op.OPCLOSURE, (1, 0)),
                    (op.OPSETGLOBAL, (1,)),
                    (op.OPGETGLOBAL, (1,)),
                    (op.OPCONSTANT, (2,)),
                    (op.OPCALL, (1,)),
                    (op.OPGETGLOBAL, (1,)),
                    (op.OPCONSTANT, (3,)),
                    (op.OPCALL, (1,)),
                    (op.OPADD, ()),
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_function_call_with_arguments_and_global(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                """
                len([]);
                """,
                (),
                [
                    # the identifier is a built-in (and thus has BUILTIN scope)
                    (op.OPGETBUILTIN, (monkey_builtins.INDEX_MONKEY_BUILTIN_LEN,)),
                    # we prepare to create an array; we still need to emit an OPARRAY instruction
                    # even if there are no arguments
                    (op.OPARRAY, (0,)),
                    # we call the builtin
                    (op.OPCALL, (1,)),
                    # we have an expression statement; need to pop it off the stack
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                """
                push([], 1);
                """,
                (1,),
                [
                    # the identifier is a built-in (and thus has BUILTIN scope)
                    (op.OPGETBUILTIN, (monkey_builtins.INDEX_MONKEY_BUILTIN_PUSH,)),
                    # we prepare to create an array; we still need to emit an OPARRAY instruction
                    # even if there are no arguments
                    (op.OPARRAY, (0,)),
                    # the `1` about to get pushed into the array needs to be put on the stack
                    # remember that the compiler loops over arguments left to right; so this has to
                    # be compiler after the array
                    (op.OPCONSTANT, (0,)),
                    # we call the builtin
                    (op.OPCALL, (2,)),
                    # we have an expression statement; need to pop it off the stack
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                """
                let ret0 = fn() {
                    return len([]);
                };
                """,
                (
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the identifier is a built-in (and thus has BUILTIN scope)
                                (op.OPGETBUILTIN, (monkey_builtins.INDEX_MONKEY_BUILTIN_LEN,)),
                                # we prepare to create an array; we still need to emit an OPARRAY instruction
                                # even if there are no arguments
                                (op.OPARRAY, (0,)),
                                # we call our builtin function, with a single argument (the empty array)
                                (op.OPCALL, (1,)),
                                # we need to return the value (pop off the function, put return value on the stack)
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # no arguments
                        0,
                    ),
                ),
                [
                    # the function itself is a constant, and it is our first (label it 0)
                    (op.OPCLOSURE, (0, 0)),
                    # the function is bound to a global name, and it is our first (label it 0)
                    (op.OPSETGLOBAL, (0,)),
                ],
            ),
        ],
    )
    def test_builtins(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                """
                fn(a) {
                    return fn(b) { a + b };
                };
                """,
                (
                    # the constant for the inner closure
                    (
                        # the bytecode instructions for the inner function
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # we go from left to right of the return value
                                # the first variable `a` is a free variable; it is the first free
                                # variable, and so gets the label 0
                                (op.OPGETFREE, (0,)),
                                # the second variable `b` is an argument, which is accessed
                                # via a local binding; it is the first argument/binding (label 0)
                                (op.OPGETLOCAL, (0,)),
                                # add the two values together, push them on the stack
                                (op.OPADD, ()),
                                # make sure this sum ends up on top of the stack after returning
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # 1 argument (`b`)
                        1,
                    ),
                    # the constant for the outer function
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the inner function uses the argument `a`, which we treat as a local binding
                                # it is this function's first and only local binding: label it 0
                                (op.OPGETLOCAL, (0,)),
                                # the return value is a closure (treated as a special type of constant)
                                # it gets its own opcode (OPCLOSURE)
                                # it is the first (0th) constant seen so far (first operand is 0)
                                # it takes one free variable (second operand is 1)
                                (op.OPCLOSURE, (0, 1)),
                                # make sure this closure ends up at the top of the stack after returning
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # 1 argument (`a`)
                        1,
                    ),
                ),
                [
                    # this value is a closure (treated as a special type of constant)
                    # it gets its own opcode (OPCLOSURE)
                    # it is the second constant seen so far (first operand is label 1)
                    # it takes no free variable (second operand is 0)
                    (op.OPCLOSURE, (1, 0)),
                    # we have an expression statement; need to pop it off the stack
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                """
                fn(a) {
                    return fn(b) {
                        return fn(c) {
                            return a + b + c;
                        };
                    };
                };
                """,
                (
                    # the constant for the inner closure
                    (
                        # the bytecode instructions for the inner function
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # we go from left to right of the return value
                                # the first variable `a` is a free variable; it is the first free
                                # variable, and so gets the label 0
                                (op.OPGETFREE, (0,)),
                                # the second variable `b` is a free variable; it is the second free
                                # variable, and so gets the label 1
                                (op.OPGETFREE, (1,)),
                                # we add these two together, and put the result on top of the stack
                                (op.OPADD, ()),
                                # the third variable `c` is an argument, which is accessed
                                # via a local binding; it is the first argument/binding (label 0)
                                (op.OPGETLOCAL, (0,)),
                                # add the two values together, push them on the stack
                                (op.OPADD, ()),
                                # make sure this sum ends up on top of the stack after returning
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # 1 argument (`c`)
                        1,
                    ),
                    # the constant for the next inner function
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the first variable `a` is a free variable; it is the first free
                                # variable this function has seen, and so gets the label 0
                                (op.OPGETFREE, (0,)),
                                # the inner function uses the argument `b`, which we treat as a local binding
                                # it is this function's first and only local binding: label it 0
                                (op.OPGETLOCAL, (0,)),
                                # the return value is a closure (treated as a special type of constant)
                                # it gets its own opcode (OPCLOSURE)
                                # it is the first (0th) constant seen so far (first operand is 0)
                                # it takes two free variable (second operand is 2)
                                (op.OPCLOSURE, (0, 2)),
                                # make sure this closure ends up at the top of the stack after returning
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # 1 argument (`b`)
                        1,
                    ),
                    # the constant for the outer function
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the inner function uses the argument `a`, which we treat as a local binding
                                # it is this function's first and only local binding: label it 0
                                (op.OPGETLOCAL, (0,)),
                                # the return value is a closure (treated as a special type of constant)
                                # it gets its own opcode (OPCLOSURE)
                                # it is the eecond constant (label 1) seen so far (first operand is 1)
                                # it takes one free variable (`a`) from the POV of the outer function (second operand is 1)
                                (op.OPCLOSURE, (1, 1)),
                                # make sure this closure ends up at the top of the stack after returning
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # 1 argument (`a`)
                        1,
                    ),
                ),
                [
                    # this value is a closure (treated as a special type of constant)
                    # it gets its own opcode (OPCLOSURE)
                    # it is the third constant seen so far (first operand is label 2)
                    # it takes no free variable (second operand is 0)
                    (op.OPCLOSURE, (2, 0)),
                    # we have an expression statement; need to pop it off the stack
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                """
                let global = 55;
                fn() {
                    let a = 66;
                    return fn() {
                        let b = 77;
                        return fn() {
                            let c = 88;
                            return global + a + b + c;
                        };
                    };
                };
                """,
                (
                    # first thing we encounter is the global
                    55,
                    # before we compile the outer function, we have to compile `a`
                    66,
                    # before we compiler the next inner function, we have to compiler `b`
                    77,
                    # before we compiler the next inner function after that, we have to compiler `c`
                    88,
                    # the inner-most closure
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # get constant `c` (label 3) from the constants list, put on the stack
                                (op.OPCONSTANT, (3,)),
                                # create a local binding for `c` (it is the first, so label 0)
                                (op.OPSETLOCAL, (0,)),
                                # now to calculate the sum to be returned; from left to right
                                # : get `global` (bound to 0 in globals) and `a` (0th free variable), and add
                                (op.OPGETGLOBAL, (0,)),
                                (op.OPGETFREE, (0,)),
                                (op.OPADD, ()),
                                # : the sum is still on top of the stack; get the next free (`b`), and add
                                (op.OPGETFREE, (1,)),
                                (op.OPADD, ()),
                                # : the sum is still on top of the stack; get the next local (`c`), and add
                                (op.OPGETLOCAL, (0,)),
                                (op.OPADD, ()),
                                # after returning, make sure this ends up on top of the stack
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # one local binding (`c`)
                        1,
                        # no arguments
                        0,
                    ),
                    # the second inner-most closure
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # get constant `b` (label 2) from the constants list, put on the stack
                                (op.OPCONSTANT, (2,)),
                                # create a local binding for `b` (it is the first, so label 0)
                                (op.OPSETLOCAL, (0,)),
                                # the closure to be returned uses two of the variables we know about:
                                # in order from left to right in terms of usage inside the function:
                                # - `a` (a free variable from this closure's POV)
                                # - `b` (a local binding from this closure's POV)
                                (op.OPGETFREE, (0,)),
                                (op.OPGETLOCAL, (0,)),
                                # the value to be returned is a closure;
                                # - this closure is the 5th constant (the 4 integers have already been made constants)
                                #   - so the first argument is `4`
                                # - this closure takes 2 free variables
                                #   - the parent free variable `a`, and the current binding (`b`)
                                (op.OPCLOSURE, (4, 2)),
                                # after returning, make sure this ends up on top of the stack
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # one local binding (`b`)
                        1,
                        # no arguments
                        0,
                    ),
                    # the outer function
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # get constant `a` (label 1) from the constants list, put on the stack
                                (op.OPCONSTANT, (1,)),
                                # create a local binding for `a` (it is the first, so label 0)
                                (op.OPSETLOCAL, (0,)),
                                # the closure to be returned uses one variable we know about:
                                # in order from left to right in terms of usage inside the function:
                                # - `a` (a local variable from this closure's POV)
                                (op.OPGETLOCAL, (0,)),
                                # the value to be returned is a closure;
                                # - this closure is the 6th constant
                                #   - the 4 integers, and the inner closure, have already been made constants
                                #   - so the first argument is `5`
                                # - this closure takes 1 free variables
                                #   - the current binding `a`
                                (op.OPCLOSURE, (5, 1)),
                                # after returning, make sure this ends up on top of the stack
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # one local binding (`a`)
                        1,
                        # no arguments
                        0,
                    ),
                ),
                [
                    # the integer `55` is pushed on top of the stack, then bound to a global binding
                    (op.OPCONSTANT, (0,)),
                    (op.OPSETGLOBAL, (0,)),
                    # the function at the global scope
                    # we use OPCLOSURE, a special type of OPCONSTANT for closures
                    # there are 6 constants that get compiled before it:
                    # - the four integers `global`, `a`, `b`, `c`, as we work our way into the function
                    # - the two inner closures
                    # this outer function takes no free variables
                    (op.OPCLOSURE, (6, 0)),
                    # the outer function is written in an expression statement; we need to pop it off
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_closure(self, case: CompilerTestCase):
        perform_compiler_test_case(case)

    @pytest.mark.parametrize(
        "case",
        [
            CompilerTestCase(
                """
                let countdown = fn(x) {
                    return countdown(x - 1);
                };
                countdown(1);
                """,
                (
                    1,
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # upon trying to resolve the `countdown` identifier, the compiler will notice
                                # that it is the name of the current function, and emit this opcode
                                (op.OPCURRENTCLOSURE, ()),
                                # get the argument (treated as local binding)
                                # it is the first local binding/argument, and so is labelled 0
                                (op.OPGETLOCAL, (0,)),
                                # the `1` is the first constant encountered (label 0); put it on the stack
                                (op.OPCONSTANT, (0,)),
                                # subtract the two things on the stack
                                (op.OPSUB, ()),
                                # look up the function that corresponds to the identifer, and call it, with 1 argument
                                (op.OPCALL, (1,)),
                                # return the value; make sure the returned value is on top of the stack
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # one argument
                        1,
                    ),
                    1,
                ),
                [
                    # create a function (constant)
                    # - it is the second constant seen so far (label 1)
                    # - it uses no free variables (value 0)
                    (op.OPCLOSURE, (1, 0)),
                    # make it a global binding
                    (op.OPSETGLOBAL, (0,)),
                    # we call it on the very next line; so put it on the stack again
                    (op.OPGETGLOBAL, (0,)),
                    # put its argument (the `1`) on top of the stack
                    # this `1` is the third constant compiled so far, so it has label 2
                    (op.OPCONSTANT, (2,)),
                    # look up the function that corresponds to the identifer, and call it, with 1 argument
                    (op.OPCALL, (1,)),
                    # the function call ended up as an expression statement; pop it off the stack
                    (op.OPPOP, ()),
                ],
            ),
            CompilerTestCase(
                """
                let wrapper = fn() {
                    let countdown = fn(x) {
                        return countdown(x - 1);
                    };
                    return countdown(1);
                };
                wrapper();
                """,
                (
                    1,
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # upon trying to resolve the `countdown` identifier, the compiler will notice
                                # that it is the name of the current function, and emit this opcode
                                (op.OPCURRENTCLOSURE, ()),
                                # get the argument (treated as local binding)
                                # it is the first local binding/argument, and so is labelled 0
                                (op.OPGETLOCAL, (0,)),
                                # the `1` is the first constant encountered (label 0); put it on the stack
                                (op.OPCONSTANT, (0,)),
                                # subtract the two things on the stack
                                (op.OPSUB, ()),
                                # look up the function that corresponds to the identifer, and call it, with 1 argument
                                (op.OPCALL, (1,)),
                                # return the value; make sure the returned value is on top of the stack
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # no local bindings
                        0,
                        # one argument
                        1,
                    ),
                    1,
                    (
                        code.make_instructions_from_opcode_operand_pairs(
                            [
                                # the closure `countdown`
                                # - it is the second constant seen so far (label 1)
                                # - it uses no free variables (value 0)
                                (op.OPCLOSURE, (1, 0)),
                                # we create a local binding for it (put into the store)
                                # it is the first local binding; set it to 0
                                (op.OPSETLOCAL, (0,)),
                                # we are about to call a function; put it on top of the stack
                                (op.OPGETLOCAL, (0,)),
                                # the argument to the function (`1`) has a label of 2
                                (op.OPCONSTANT, (2,)),
                                # look up the function that corresponds to the identifer, and call it, with 1 argument
                                (op.OPCALL, (1,)),
                                # return the value; make sure the returned value is on top of the stack
                                (op.OPRETURNVALUE, ()),
                            ]
                        ),
                        # one local binding
                        1,
                        # no arguments
                        0,
                    ),
                ),
                [
                    # create a function (constant)
                    # - it is the fourth constant seen so far (label 3)
                    # - it uses no free variables (value 0)
                    (op.OPCLOSURE, (3, 0)),
                    # make it a global binding
                    (op.OPSETGLOBAL, (0,)),
                    # we call it on the very next line; so put it on the stack again
                    (op.OPGETGLOBAL, (0,)),
                    # look up the function that corresponds to the identifer, and call it
                    # - it takes no arguments (value 0)
                    (op.OPCALL, (0,)),
                    # the function call ended up as an expression statement; pop it off the stack
                    (op.OPPOP, ()),
                ],
            ),
        ],
    )
    def test_recursive_closure(self, case: CompilerTestCase):
        perform_compiler_test_case(case)


# NOTE TO DEV: the number of locals in a function is the unique number of variables
# that are defined in the function's body; not every constant gets a binding, so the
# constants that are just expression statements on their own do not count towards
# the number of local bindings
