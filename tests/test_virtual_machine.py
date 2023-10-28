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
    @pytest.mark.parametrize(
        "test_case",
        [
            VirtualMachineTestCase("0;", 0),
            VirtualMachineTestCase("1;", 1),
            VirtualMachineTestCase("1 + 2;", 3),
            VirtualMachineTestCase("1 - 2;", -1),
            VirtualMachineTestCase("2 * 3;", 6),
            VirtualMachineTestCase("6 / 3;", 2),
            VirtualMachineTestCase("6 / 4;", 1),
        ],
    )
    def test_basic(self, test_case: VirtualMachineTestCase):
        program = compiler_utils.parse(test_case.input_text)
        compiler = comp.Compiler()
        comp.compile(compiler, program)

        bytecode = comp.bytecode_from_compiler(compiler)
        machine = vm.VirtualMachine(bytecode)
        vm.run(machine)

        top_object = machine.stack.maybe_get_last_popped()
        assert top_object is not None
        assert object_utils.is_expected_object(top_object, test_case.expected)
