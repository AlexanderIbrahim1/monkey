"""
This module contains the VirtualMachine class, which runs the Bytecode instance that is
emitted by the compiler.
"""

from typing import Optional

import monkey.code as code
import monkey.code.opcodes as opcodes
import monkey.compiler as comp
import monkey.object as objs

from monkey.virtual_machine.constants import MAX_STACK_SIZE
from monkey.containers import FixedStack


class VirtualMachine:
    def __init__(self, bytecode: comp.Bytecode) -> None:
        self._bytecode = bytecode
        self._stack = FixedStack[objs.Object](MAX_STACK_SIZE)
        pass

    @property
    def bytecode(self) -> comp.Bytecode:
        return self._bytecode

    def stack_top(self) -> Optional[objs.Object]:
        return self._stack.maybe_peek()

    def push(self, obj: objs.Object) -> None:
        self._stack.push(obj)


def run(vm: VirtualMachine) -> None:
    instructions = vm.bytecode.instructions

    instr_ptr = 0
    while instr_ptr < len(instructions):
        opcode = code.Opcode(instructions[instr_ptr])

        match opcode:
            case opcodes.OPCONSTANT:
                instr_ptr += _push_opconstant(vm, instr_ptr)


def _push_opconstant(vm: VirtualMachine, instr_ptr: int) -> int:
    position = _read_position(vm, instr_ptr, opcodes.OPCONSTANT_WIDTH)
    constant = vm.bytecode.constants[position]
    vm.push(constant)

    return opcodes.OPCONSTANT_WIDTH


def _read_position(vm: VirtualMachine, instr_ptr: int, size: int) -> int:
    begin_ptr = instr_ptr + 1
    end_ptr = begin_ptr + size
    position_bytes = vm.bytecode.instructions[begin_ptr:end_ptr]
    return int.from_bytes(position_bytes, byteorder="big", signed=False)
