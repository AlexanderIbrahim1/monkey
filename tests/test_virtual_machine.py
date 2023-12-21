import dataclasses
from typing import Any

import pytest

import monkey.compiler as comp
import monkey.virtual_machine as vm

import compiler_utils
import object_utils


@dataclasses.dataclass
class VirtualMachineTestCase:
    input_text: str
    expected: Any


class TestVirtualMachine:
    # NOTE: we don't have to implement anything to do with priorities to get the parentheses
    #       to work properly; this is because the parser has already taken care of that, and
    #       turned the stuff inside the parentheses into objects to be compared! The VM only
    #       works with the Object instance that the parser has already created!
    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("0;", 0),
            VirtualMachineTestCase("1;", 1),
            VirtualMachineTestCase("true;", True),
            VirtualMachineTestCase("false;", False),
        ],
    )
    def test_literal_expression_statement(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("1 + 2;", 3),
            VirtualMachineTestCase("1 - 2;", -1),
            VirtualMachineTestCase("2 * 3;", 6),
            VirtualMachineTestCase("6 / 3;", 2),
            VirtualMachineTestCase("6 / 4;", 1),
        ],
    )
    def test_arithmetic_infix_operator(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("1 > 2;", False),
            VirtualMachineTestCase("2 < 1;", False),
            VirtualMachineTestCase("1 < 2;", True),
            VirtualMachineTestCase("2 > 1;", True),
            VirtualMachineTestCase("1 == 1;", True),
            VirtualMachineTestCase("1 != 1;", False),
            VirtualMachineTestCase("2 == 1;", False),
            VirtualMachineTestCase("2 != 1;", True),
        ],
    )
    def test_integer_comparison_operator(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("true == true;", True),
            VirtualMachineTestCase("false == false;", True),
            VirtualMachineTestCase("true == false;", False),
            VirtualMachineTestCase("true != true;", False),
            VirtualMachineTestCase("false != false;", False),
            VirtualMachineTestCase("true != false;", True),
        ],
    )
    def test_boolean_literal_comparison_operator(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("(1 < 2) == true;", True),
            VirtualMachineTestCase("(1 < 2) == false;", False),
            VirtualMachineTestCase("(1 > 2) == true;", False),
            VirtualMachineTestCase("(1 > 2) == false;", True),
        ],
    )
    def test_infix_expression_equals_boolean_literal(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("-5;", -5),
            VirtualMachineTestCase("-10;", -10),
            VirtualMachineTestCase("-0;", 0),
        ],
    )
    def test_minus_prefix_integer_operator(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("!true;", False),
            VirtualMachineTestCase("!!true;", True),
            VirtualMachineTestCase("!false;", True),
            VirtualMachineTestCase("!!false;", False),
            VirtualMachineTestCase("!123;", False),
            VirtualMachineTestCase("!!123;", True),
            VirtualMachineTestCase("!true == false;", True),
        ],
    )
    def test_bang_prefix_boolean_operator(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("-10 + 20;", 10),
            VirtualMachineTestCase("-10 + 20 - 10;", 0),
            VirtualMachineTestCase("-(10 + 20);", -30),
            VirtualMachineTestCase("-(10 + 20) + 25;", -5),
            VirtualMachineTestCase("-(10 + 20) / 5 + 1;", -5),
        ],
    )
    def test_minus_sign_with_arithmetic_operations(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("if (true) { 10 };", 10),
            VirtualMachineTestCase("if (true) { 10 } else { 20 };", 10),
            VirtualMachineTestCase("if (false) { 10 } else { 20 };", 20),
            VirtualMachineTestCase("if (1) { 10 };", 10),
            VirtualMachineTestCase("if (1 < 2) { 10 };", 10),
            VirtualMachineTestCase("if (1 < 2) { 10 } else { 20 };", 10),
            VirtualMachineTestCase("if (1 > 2) { 10 } else { 20 };", 20),
            VirtualMachineTestCase("if (false) { 10 };", None),
            VirtualMachineTestCase("!(if (false) { 10 });", True),
            VirtualMachineTestCase("if ( (if (false) { 10 }) ) { 10 } else { 20 };", 20),
        ],
    )
    def test_if_else_expression(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("let one = 1; one;", 1),
            VirtualMachineTestCase("let one = 1; let two = 2; one + two;", 3),
            VirtualMachineTestCase("let one = 1; let two = one + one; one + two;", 3),
        ],
    )
    def test_let_statement(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase('"monkey";', "monkey"),
            VirtualMachineTestCase('"mon" + "key";', "monkey"),
            VirtualMachineTestCase('"mon" + "key" + " banana";', "monkey banana"),
        ],
    )
    def test_string_literals(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("[];", []),
            VirtualMachineTestCase("[1, 2, 3];", [1, 2, 3]),
            VirtualMachineTestCase("[1 + 2, 3 - 4, 5 * 6];", [3, -1, 30]),
        ],
    )
    def test_array_literals(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("{};", {}),
            VirtualMachineTestCase("{1: 2, 2: 3};", {1: 2, 2: 3}),
            VirtualMachineTestCase("{1: 2, 3: 4};", {1: 2, 3: 4}),
            VirtualMachineTestCase("{1 + 1: 2 * 2, 3 - 3: 4 / 4};", {2: 4, 0: 1}),
        ],
    )
    def test_hash_literals(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("[1, 2, 3][1];", 2),
            VirtualMachineTestCase("[1, 2, 3][0 + 2];", 3),
            VirtualMachineTestCase("[[1, 3, 5]][0][0];", 1),
            VirtualMachineTestCase("[[1, 3, 5]][0][0];", 1),
        ],
    )
    def test_array_indexing(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case_input_text",
        [
            "[1, 2, 3][3];",
            "[][0];",
            "[][1];",
            "[1, 2, 3, 4][-1];",
        ],
    )
    def test_array_index_raises(self, test_case_input_text: str):
        virtual_machine_test_case_raises_internals(test_case_input_text)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("{1: 2, 3: 4}[1];", 2),
            VirtualMachineTestCase("{1: 2, 3: 4}[3];", 4),
            VirtualMachineTestCase("{1: 2, 3: 4}[1 + 2];", 4),
            VirtualMachineTestCase("{1: 2, 1 + 2: 4}[3];", 4),
            VirtualMachineTestCase("{true: 5, false: 10, 7: 123}[true];", 5),
            VirtualMachineTestCase("{true: 5, false: 10, 7: 123}[false];", 10),
            VirtualMachineTestCase("{true: 5, false: 10, 7: 123}[7];", 123),
        ],
    )
    def test_hash_indexing(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case_input_text",
        [
            "{1: 2}[3];",
            "{1: 2}[0];",
            "{}[0];",
        ],
    )
    def test_hash_index_raises(self, test_case_input_text: str):
        virtual_machine_test_case_raises_internals(test_case_input_text)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("fn() { 5 + 10 }();", 15),
            VirtualMachineTestCase("let my_func = fn() { 5 + 10 }; my_func();", 15),
            VirtualMachineTestCase(
                """
                let one = fn() { return 1; };
                let two = fn() { return 2; };
                one() + two();
                """,
                3,
            ),
            VirtualMachineTestCase(
                """
                let a = fn() { 1 };
                let b = fn() { a() + 1 };
                let c = fn() { b() + 1 };
                c();
                """,
                3,
            ),
            VirtualMachineTestCase(
                """
                let early_exit = fn() { return 99; 100; };
                early_exit();
                """,
                99,
            ),
            VirtualMachineTestCase(
                """
                let early_exit = fn() { return 99; return 100; };
                early_exit();
                """,
                99,
            ),
        ],
    )
    def test_function_call_no_arguments(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase(
                """
                let no_return = fn() {};
                no_return();
                """,
                None,
            ),
            VirtualMachineTestCase(
                """
                let no_return = fn() {};
                let no_return_two = fn() { no_return(); };
                no_return();
                no_return_two();
                """,
                None,
            ),
        ],
    )
    def test_function_call_no_return_value_no_arguments(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase(
                """
                let returns_one = fn() { return 1; };
                let returns_returns_one = fn() { return returns_one; };
                returns_returns_one()();
                """,
                1,
            )
        ],
    )
    def test_function_call_return_function(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase(
                """
                let one = fn() {
                    let one = 1;
                    return one;
                };
                one();
                """,
                1,
            ),
            VirtualMachineTestCase(
                """
                let one_and_two = fn() {
                    let one = 1;
                    let two = 2;
                    return one + two;
                };
                one_and_two();
                """,
                3,
            ),
            VirtualMachineTestCase(
                """
                let one_and_two = fn() {
                    let one = 1;
                    let two = 2;
                    return one + two;
                };
                one_and_two();
                """,
                3,
            ),
            VirtualMachineTestCase(
                """
                let one_and_two = fn() {
                    let one = 1;
                    let two = 2;
                    return one + two;
                };
                let three_and_four = fn() {
                    let three = 3;
                    let four = 4;
                    return three + four;
                };
                one_and_two() + three_and_four();
                """,
                10,
            ),
            VirtualMachineTestCase(
                """
                let first_foobar = fn() {
                    let foobar = 50;
                    foobar;
                };
                let second_foobar = fn() {
                    let foobar = 100;
                    foobar;
                };
                first_foobar() + second_foobar();
                """,
                150,
            ),
            VirtualMachineTestCase(
                """
                let global_seed = 50;
                let minus_one = fn() {
                    let num = 1;
                    return global_seed - num;
                };
                let minus_two = fn() {
                    let num = 2;
                    return global_seed - num;
                };
                minus_one() + minus_two();
                """,
                97,
            ),
        ],
    )
    def test_function_call_with_local_bindings(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase(
                """
                let identity = fn(a) { return a; };
                identity(5);
                """,
                5,
            ),
            VirtualMachineTestCase(
                """
                let sum = fn(a, b) { a + b };
                sum(1, 2);
                """,
                3,
            ),
            VirtualMachineTestCase(
                """
                let sum = fn(a, b) {
                    let c = a + b;
                    return c;
                };
                sum(1, 2);
                """,
                3,
            ),
            VirtualMachineTestCase(
                """
                let sum = fn(a, b) {
                    let c = a + b;
                    return c;
                };
                sum(1, 2) + sum(3, 4);
                """,
                10,
            ),
            VirtualMachineTestCase(
                """
                let sum = fn(a, b) {
                    let c = a + b;
                    return c;
                };
                let outer = fn() {
                    sum(1, 2) + sum(3, 4)
                };
                outer();
                """,
                10,
            ),
            VirtualMachineTestCase(
                """
                let global_num = 10;
                let sum_with_global = fn(a, b) {
                    let c = a + b;
                    let s = c + global_num;
                    return s;
                };
                sum_with_global(1, 2);
                """,
                13,
            ),
            VirtualMachineTestCase(
                """
                let global_num = 10;
                let sum_with_global = fn(a, b) {
                    let c = a + b;
                    let s = c + global_num;
                    return s;
                };
                let value = sum_with_global(1, 2);
                value;
                """,
                13,
            ),
        ],
    )
    def test_function_call_with_arguments(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)

    @pytest.mark.skip
    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase(
                """
                let global_num = 10;
                let sum_with_global_twice = fn(a) {
                    return a + global_num + global_num;
                };
                sum_with_global_twice(5);
                """,
                25,
            ),
            VirtualMachineTestCase(
                """
                let global_num = 10;
                let sum_with_global = fn(a) {
                    return a + global_num;
                };
                sum_with_global(1) + sum_with_global(2);
                """,
                23,
            ),
            #            VirtualMachineTestCase(
            #                """
            #                let global_num = 10;
            #                let sum_with_global = fn(a, b) {
            #                    let c = a + b;
            #                    let s = c + global_num;
            #                    return s;
            #                };
            #                let value0 = sum_with_global(1, 2);
            #                let value1 = sum_with_global(3, 4);
            #                value0 + value1;
            #                """,
            #                30,
            #            ),
        ],
    )
    def test_function_call_with_arguments_twice(self, test_case: VirtualMachineTestCase):
        virtual_machine_test_case_internals(test_case)


def virtual_machine_test_case_internals(test_case: VirtualMachineTestCase):
    """
    Assert that, after compilation and runnning by the VM, that the top object
    on the stack is what you expect.

    This method is so general for the test suite that all the tests end up using the
    same body, with very little to no variation. As a result, it becomes difficult to
    sort the different types of tests.

    By extracting the body of the testing code into its own function, we can separate
    the test cases into other functions with more descriptive names, allowing us to
    be better organized.
    """
    program = compiler_utils.parse(test_case.input_text)
    compiler = comp.Compiler()
    comp.compile(compiler, program)

    bytecode = comp.bytecode_from_compiler(compiler)
    machine = vm.VirtualMachine(bytecode)
    vm.run(machine)

    top_object = machine.stack.maybe_get_last_popped()
    assert top_object is not None
    assert object_utils.is_expected_object(top_object, test_case.expected)


def virtual_machine_test_case_raises_internals(input_text: str):
    """
    Assert that, after compilation and runnning by the VM, that a VirtualMachineError
    is raised.
    """
    program = compiler_utils.parse(input_text)
    compiler = comp.Compiler()
    comp.compile(compiler, program)

    bytecode = comp.bytecode_from_compiler(compiler)
    machine = vm.VirtualMachine(bytecode)

    with pytest.raises(vm.VirtualMachineError):
        vm.run(machine)
