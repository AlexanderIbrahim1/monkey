"""
This module contains the VirtualMachine class, which runs the Bytecode instance that is
emitted by the compiler.
"""

import dataclasses

import monkey.code as code
import monkey.code.opcodes as opcodes
import monkey.compiler as comp
import monkey.object as objs

from monkey.containers import FixedStack
from monkey.virtual_machine.constants import MAX_STACK_SIZE
from monkey.virtual_machine.custom_exceptions import VirtualMachineError


@dataclasses.dataclass
class VirtualMachine:
    bytecode: comp.Bytecode
    stack: FixedStack[objs.Object] = FixedStack[objs.Object](MAX_STACK_SIZE)


def run(vm: VirtualMachine) -> None:
    instructions = vm.bytecode.instructions

    instr_ptr = 0
    while instr_ptr < len(instructions):
        opcode = code.extract_opcode(instructions, instr_ptr)

        match opcode:
            case opcodes.OPCONSTANT:
                instr_ptr += _push_opconstant(vm, instr_ptr)
            case opcodes.OPADD:
                _push_opadd(vm)
            case opcodes.OPPOP:
                vm.stack.pop()
            case _:
                raise VirtualMachineError(f"Could not find a matching opcode: Found: {opcode!r}")

        instr_ptr += 1


def _pop_integer(vm: VirtualMachine) -> int:
    integer = vm.stack.pop()
    match integer:
        case objs.IntegerObject(value):
            return value
        case _:
            raise VirtualMachineError(
                "Expected to pop an 'int'\n" f"Found instance of {type(integer)}, with value {integer}"
            )


def _push_opadd(vm: VirtualMachine) -> None:
    right_value = _pop_integer(vm)
    left_value = _pop_integer(vm)
    result = right_value + left_value

    integer = objs.IntegerObject(result)
    vm.stack.push(integer)


def _push_opconstant(vm: VirtualMachine, instr_ptr: int) -> int:
    position = _read_position(vm, instr_ptr, opcodes.OPCONSTANT_WIDTH)
    constant = vm.bytecode.constants[position]
    vm.stack.push(constant)

    return opcodes.OPCONSTANT_WIDTH


def _read_position(vm: VirtualMachine, instr_ptr: int, size: int) -> int:
    begin_ptr = instr_ptr + 1
    end_ptr = begin_ptr + size
    position_bytes = vm.bytecode.instructions[begin_ptr:end_ptr]
    return int.from_bytes(position_bytes, byteorder="big", signed=False)
