"""
This module contains the VirtualMachine class, which runs the Bytecode instance that is
emitted by the compiler.
"""

import dataclasses

import monkey.code as code
import monkey.code.opcodes as opcodes
import monkey.compiler as comp
import monkey.object as objs

from monkey.tokens import token_types
from monkey.object.object_type import OBJECT_TYPE_DICT

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
                _push_op_add(vm)
            case opcodes.OPSUB:
                _push_op_sub(vm)
            case opcodes.OPMUL:
                _push_op_mul(vm)
            case opcodes.OPDIV:
                _push_op_div(vm)
            case opcodes.OPPOP:
                vm.stack.pop()
            case opcodes.OPTRUE:
                vm.stack.push(objs.TRUE_BOOL_OBJ)
            case opcodes.OPFALSE:
                vm.stack.push(objs.FALSE_BOOL_OBJ)
            case opcodes.OPEQUAL:
                _push_op_equal(vm)
            case opcodes.OPNOTEQUAL:
                _push_op_notequal(vm)
            case opcodes.OPGREATERTHAN:
                _push_op_greaterthan(vm)
            case _:
                raise VirtualMachineError(f"Could not find a matching opcode: Found: {opcode!r}")

        instr_ptr += 1


def _push_op_add(vm: VirtualMachine) -> None:
    right_object = vm.stack.pop()
    left_object = vm.stack.pop()

    match (left_object, right_object):
        case (objs.IntegerObject(), objs.IntegerObject()):
            left_value = left_object.value
            right_value = right_object.value
            result = left_value + right_value
            integer = objs.IntegerObject(result)
            vm.stack.push(integer)
        case _:
            err_msg = _invalid_infix_operation_error(token_types.PLUS, left_object, right_object)
            raise VirtualMachineError(err_msg)


def _push_op_sub(vm: VirtualMachine) -> None:
    right_object = vm.stack.pop()
    left_object = vm.stack.pop()

    match (left_object, right_object):
        case (objs.IntegerObject(), objs.IntegerObject()):
            left_value = left_object.value
            right_value = right_object.value
            result = left_value - right_value
            integer = objs.IntegerObject(result)
            vm.stack.push(integer)
        case _:
            err_msg = _invalid_infix_operation_error(token_types.MINUS, left_object, right_object)
            raise VirtualMachineError(err_msg)


def _push_op_mul(vm: VirtualMachine) -> None:
    right_object = vm.stack.pop()
    left_object = vm.stack.pop()

    match (left_object, right_object):
        case (objs.IntegerObject(), objs.IntegerObject()):
            left_value = left_object.value
            right_value = right_object.value
            result = left_value * right_value
            integer = objs.IntegerObject(result)
            vm.stack.push(integer)
        case _:
            err_msg = _invalid_infix_operation_error(token_types.ASTERISK, left_object, right_object)
            raise VirtualMachineError(err_msg)


def _push_op_div(vm: VirtualMachine) -> None:
    right_object = vm.stack.pop()
    left_object = vm.stack.pop()

    match (left_object, right_object):
        case (objs.IntegerObject(), objs.IntegerObject()):
            left_value = left_object.value
            right_value = right_object.value
            result = left_value // right_value
            integer = objs.IntegerObject(result)
            vm.stack.push(integer)
        case _:
            err_msg = _invalid_infix_operation_error(token_types.SLASH, left_object, right_object)
            raise VirtualMachineError(err_msg)


def _push_op_equal(vm: VirtualMachine) -> None:
    right_object = vm.stack.pop()
    left_object = vm.stack.pop()

    match (left_object, right_object):
        case (objs.IntegerObject(), objs.IntegerObject()) | (objs.BooleanObject(), objs.BooleanObject()):
            left_value = left_object.value
            right_value = right_object.value
            if left_value == right_value:
                vm.stack.push(objs.TRUE_BOOL_OBJ)
            else:
                vm.stack.push(objs.FALSE_BOOL_OBJ)
        case _:
            err_msg = _invalid_infix_operation_error(token_types.EQ, left_object, right_object)
            raise VirtualMachineError(err_msg)


def _push_op_notequal(vm: VirtualMachine) -> None:
    right_object = vm.stack.pop()
    left_object = vm.stack.pop()

    match (left_object, right_object):
        case (objs.IntegerObject(), objs.IntegerObject()) | (objs.BooleanObject(), objs.BooleanObject()):
            left_value = left_object.value
            right_value = right_object.value
            if left_value != right_value:
                vm.stack.push(objs.TRUE_BOOL_OBJ)
            else:
                vm.stack.push(objs.FALSE_BOOL_OBJ)
        case _:
            err_msg = _invalid_infix_operation_error(token_types.NOT_EQ, left_object, right_object)
            raise VirtualMachineError(err_msg)


def _push_op_greaterthan(vm: VirtualMachine) -> None:
    right_object = vm.stack.pop()
    left_object = vm.stack.pop()

    match (left_object, right_object):
        case (objs.IntegerObject(), objs.IntegerObject()):
            left_value = left_object.value
            right_value = right_object.value
            if left_value > right_value:
                vm.stack.push(objs.TRUE_BOOL_OBJ)
            else:
                vm.stack.push(objs.FALSE_BOOL_OBJ)
        case _:
            err_msg = _invalid_infix_operation_error(token_types.GT, left_object, right_object)
            raise VirtualMachineError(err_msg)


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


def _invalid_infix_operation_error(operation: str, left_obj: objs.Object, right_obj: objs.Object) -> str:
    left_str = OBJECT_TYPE_DICT[left_obj.data_type()]
    right_str = OBJECT_TYPE_DICT[right_obj.data_type()]
    message = f"Unable to perform '{operation}' on objects of type '{left_str}' and '{right_str}'"

    return message
