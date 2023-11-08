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
