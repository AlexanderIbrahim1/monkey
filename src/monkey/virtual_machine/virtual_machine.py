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
    globals: FixedStack[objs.Object] = FixedStack[objs.Object](MAX_STACK_SIZE)


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
            case opcodes.OPMINUS:
                _push_op_minus(vm)
            case opcodes.OPBANG:
                _push_op_bang(vm)
            case opcodes.OPJUMP:
                instr_ptr = _new_position_after_jump(vm, instr_ptr)
            case opcodes.OPJUMPWHENFALSE:
                instr_ptr = _new_position_after_jump_when_false(vm, instr_ptr)
            case opcodes.OPNULL:
                vm.stack.push(objs.NULL_OBJ)
            case opcodes.OPSETGLOBAL:
                i_global = _global_identifier_index(instructions, instr_ptr)
                instr_ptr += opcodes.OPSETGLOBAL_WIDTH

                # remember that a let statement first pushes something onto the stack, and then
                # we assign it to a particular variable
                value_to_bind = vm.stack.pop()

                if i_global >= vm.globals.size():
                    vm.globals.push(value_to_bind)
                else:
                    vm.globals[i_global] = value_to_bind
            case opcodes.OPGETGLOBAL:
                i_global = _global_identifier_index(instructions, instr_ptr)
                instr_ptr += opcodes.OPSETGLOBAL_WIDTH

                # the identifier we want to reference could be anywhere in the globals stack, not
                # just at the top; so we can't pop or anything
                bound_value = vm.globals[i_global]
                vm.stack.push(bound_value)
            case opcodes.OPARRAY:
                # the operand of the OPARRAY opcode is the number of elements in the array
                n_elements = _number_of_array_elements(instructions, instr_ptr)
                instr_ptr += opcodes.OPARRAY_WIDTH

                i_first_element = vm.stack.size() - n_elements
                array = _build_array(vm, i_first_element, n_elements)

                # we go back to the position of the first element
                vm.stack.shrink_stack_pointer(n_elements)

                vm.stack.push(array)
            case opcodes.OPHASH:
                # the operand of the OPHASH opcode is (twice) the number of elements in the hashmap
                n_objects = _number_of_hash_objects(instructions, instr_ptr)
                instr_ptr += opcodes.OPHASH_WIDTH

                i_first_element = vm.stack.size() - n_objects
                hashmap = _build_hashmap(vm, i_first_element, n_objects)

                # we go back to the position of the first element
                vm.stack.shrink_stack_pointer(n_objects)

                vm.stack.push(hashmap)
            case _:
                raise VirtualMachineError(f"Could not find a matching opcode: Found: {opcode!r}")

        instr_ptr += 1


def _build_hashmap(vm: VirtualMachine, i_start: int, n_objects: int) -> objs.HashObject:
    hashmap: dict[objs.ObjectHash, objs.HashKeyValuePair] = {}

    # the keys and values come in consecutive pairs, and each counts as an object, so we need
    # to move forward in pairs
    for i in range(0, n_objects, 2):
        key_position = i + i_start
        value_position = i + i_start + 1
        key = vm.stack[key_position]
        value = vm.stack[value_position]

        hashvalue = objs.create_object_hash(key)
        pair = objs.HashKeyValuePair(key, value)

        hashmap[hashvalue] = pair

    return objs.HashObject(hashmap)


def _number_of_hash_objects(instructions: code.Instructions, instr_ptr: int) -> int:
    hash_size_position = instr_ptr + 1
    size_bytes = code.extract_operand(instructions, hash_size_position, opcodes.OPHASH_WIDTH)
    n_objects = int.from_bytes(size_bytes, byteorder="big", signed=False)

    return n_objects


def _build_array(vm: VirtualMachine, i_start: int, n_elements: int) -> objs.ArrayObject:
    elements: list[objs.Object] = [vm.stack[i + i_start] for i in range(n_elements)]

    return objs.ArrayObject(elements)


def _number_of_array_elements(instructions: code.Instructions, instr_ptr: int) -> int:
    array_size_position = instr_ptr + 1
    size_bytes = code.extract_operand(instructions, array_size_position, opcodes.OPARRAY_WIDTH)
    n_elements = int.from_bytes(size_bytes, byteorder="big", signed=False)

    return n_elements


def _global_identifier_index(instructions: code.Instructions, instr_ptr: int) -> int:
    global_label_position = instr_ptr + 1
    position_bytes = code.extract_operand(instructions, global_label_position, opcodes.OPSETGLOBAL_WIDTH)
    position = int.from_bytes(position_bytes, byteorder="big", signed=False)

    return position


def _new_position_after_jump(vm: VirtualMachine, instr_ptr: int) -> int:
    instructions = vm.bytecode.instructions
    jump_position_bytes = code.extract_operand(instructions, instr_ptr + 1, opcodes.OPJUMP_WIDTH)
    jump_position = int.from_bytes(jump_position_bytes)

    return jump_position - 1


def _new_position_after_jump_when_false(vm: VirtualMachine, instr_ptr: int) -> int:
    condition = vm.stack.pop()

    if not objs.is_truthy(condition):
        instructions = vm.bytecode.instructions
        jump_position_bytes = code.extract_operand(instructions, instr_ptr + 1, opcodes.OPJUMPWHENFALSE_WIDTH)
        jump_position = int.from_bytes(jump_position_bytes)
        new_instr_ptr = jump_position - 1
    else:
        new_instr_ptr = instr_ptr + opcodes.OPJUMPWHENFALSE_WIDTH

    return new_instr_ptr


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
        case (objs.StringObject(), objs.StringObject()):
            left_value = left_object.value
            right_value = right_object.value
            result = left_value + right_value
            integer = objs.StringObject(result)
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


def _push_op_minus(vm: VirtualMachine) -> None:
    argument = vm.stack.pop()

    match argument:
        case objs.IntegerObject():
            value = argument.value
            integer = objs.IntegerObject(-value)
            vm.stack.push(integer)
        case _:
            err_msg = _invalid_prefix_operation_error(token_types.MINUS, argument)
            raise VirtualMachineError(err_msg)


def _push_op_bang(vm: VirtualMachine) -> None:
    argument = vm.stack.pop()

    match argument:
        case objs.BooleanObject():
            value = argument.value
            if value:
                vm.stack.push(objs.FALSE_BOOL_OBJ)
            else:
                vm.stack.push(objs.TRUE_BOOL_OBJ)
        case objs.NULL_OBJ:
            vm.stack.push(objs.TRUE_BOOL_OBJ)
        case _:
            vm.stack.push(objs.FALSE_BOOL_OBJ)


def _read_position(vm: VirtualMachine, instr_ptr: int, size: int) -> int:
    begin_ptr = instr_ptr + 1
    end_ptr = begin_ptr + size
    position_bytes = vm.bytecode.instructions[begin_ptr:end_ptr]
    return int.from_bytes(position_bytes, byteorder="big", signed=False)


def _invalid_infix_operation_error(operation: str, left_obj: objs.Object, right_obj: objs.Object) -> str:
    left_str = OBJECT_TYPE_DICT[left_obj.data_type()]
    right_str = OBJECT_TYPE_DICT[right_obj.data_type()]
    message = f"Unable to perform infix '{operation}' on objects of type '{left_str}' and '{right_str}'"

    return message


def _invalid_prefix_operation_error(operation: str, argument: objs.Object) -> str:
    argument_str = OBJECT_TYPE_DICT[argument.data_type()]
    message = f"Unable to perform prefix operation '{operation}' on object of type '{argument_str}'"

    return message
