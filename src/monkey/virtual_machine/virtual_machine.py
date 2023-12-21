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
from monkey.virtual_machine.constants import DUMMY_MAIN_FUNCTION_NUMBER_OF_LOCALS
from monkey.virtual_machine.constants import MAX_VM_STACK_SIZE
from monkey.virtual_machine.constants import MAX_VM_GLOBALS_SIZE
from monkey.virtual_machine.constants import MAX_VM_FRAME_SIZE
from monkey.virtual_machine.custom_exceptions import VirtualMachineError
from monkey.virtual_machine.stack_frame import StackFrame


@dataclasses.dataclass
class VirtualMachine:
    def __init__(self, bytecode: comp.Bytecode) -> None:
        self.globals = FixedStack[objs.Object](MAX_VM_GLOBALS_SIZE)
        self.frames = FixedStack[StackFrame](MAX_VM_FRAME_SIZE)
        self.constants = bytecode.constants

        dummy_value = DUMMY_MAIN_FUNCTION_NUMBER_OF_LOCALS
        main_function = objs.CompiledFunctionObject(bytecode.instructions, dummy_value)
        main_frame = StackFrame(main_function, base_pointer=0)
        self.frames.push(main_frame)

        self.stack = FixedStack[objs.Object](MAX_VM_STACK_SIZE, default_element_factory=objs.DefaultObject)

    @property
    def instructions(self) -> code.Instructions:
        return self.frames.peek().instructions

    @property
    def instruction_pointer(self) -> int:
        return self.frames.peek().instruction_pointer

    @instruction_pointer.setter
    def instruction_pointer(self, other: int) -> None:
        self.frames.peek().instruction_pointer = other


def run(vm: VirtualMachine) -> None:
    while vm.instruction_pointer < len(vm.instructions) - 1:
        vm.instruction_pointer += 1
        opcode = code.extract_opcode(vm.instructions, vm.instruction_pointer)
        print(f"STACK: {vm.stack._data[:vm.stack.size()]}")
        print(f"OPCODE: {code.lookup_opcode_definition(opcode).name}")

        match opcode:
            case opcodes.OPCONSTANT:
                vm.instruction_pointer += _push_opconstant(vm, vm.instruction_pointer)
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
                vm.instruction_pointer = _new_position_after_jump(vm, vm.instruction_pointer)
            case opcodes.OPJUMPWHENFALSE:
                vm.instruction_pointer = _new_position_after_jump_when_false(vm, vm.instruction_pointer)
            case opcodes.OPNULL:
                vm.stack.push(objs.NULL_OBJ)
            case opcodes.OPSETGLOBAL:
                i_global = _global_identifier_index(vm.instructions, vm.instruction_pointer)
                vm.instruction_pointer += opcodes.OPSETGLOBAL_WIDTH

                # remember that a let statement first pushes something onto the stack, and then
                # we assign it to a particular variable
                value_to_bind = vm.stack.pop()

                if i_global >= vm.globals.size():
                    vm.globals.push(value_to_bind)
                else:
                    vm.globals[i_global] = value_to_bind
            case opcodes.OPGETGLOBAL:
                i_global = _global_identifier_index(vm.instructions, vm.instruction_pointer)
                vm.instruction_pointer += opcodes.OPSETGLOBAL_WIDTH

                # the identifier we want to reference could be anywhere in the globals stack, not
                # just at the top; so we can't pop or anything
                bound_value = vm.globals[i_global]
                vm.stack.push(bound_value)
            case opcodes.OPSETLOCAL:
                i_local = _local_identifier_index(vm.instructions, vm.instruction_pointer)
                vm.instruction_pointer += opcodes.OPSETLOCAL_WIDTH

                current_frame = vm.frames.peek()
                base_pointer = current_frame.base_pointer
                local_pointer = base_pointer + i_local

                vm.stack[local_pointer] = vm.stack.pop()
            case opcodes.OPGETLOCAL:
                i_local = _local_identifier_index(vm.instructions, vm.instruction_pointer)
                vm.instruction_pointer += opcodes.OPSETLOCAL_WIDTH

                current_frame = vm.frames.peek()
                base_pointer = current_frame.base_pointer
                local_pointer = base_pointer + i_local

                object_to_push = vm.stack[local_pointer]
                vm.stack.push(object_to_push)
            case opcodes.OPARRAY:
                # the operand of the OPARRAY opcode is the number of elements in the array
                n_elements = _number_of_array_elements(vm.instructions, vm.instruction_pointer)
                vm.instruction_pointer += opcodes.OPARRAY_WIDTH

                i_first_element = vm.stack.size() - n_elements
                array = _build_array(vm, i_first_element, n_elements)

                # we go back to the position of the first element
                vm.stack.shrink_stack_pointer(n_elements)

                vm.stack.push(array)
            case opcodes.OPHASH:
                # the operand of the OPHASH opcode is (twice) the number of elements in the hashmap
                n_objects = _number_of_hash_objects(vm.instructions, vm.instruction_pointer)
                vm.instruction_pointer += opcodes.OPHASH_WIDTH

                i_first_element = vm.stack.size() - n_objects
                hashmap = _build_hashmap(vm, i_first_element, n_objects)

                # we go back to the position of the first element
                vm.stack.shrink_stack_pointer(n_objects)

                vm.stack.push(hashmap)
            case opcodes.OPINDEX:
                # when an index expression `container[inside]` is compiled, what happens is:
                # - `container`` is compiled first
                # - `inside` is compiled next (and is on top of the stack)
                # - the `OPINDEX` instruction is pushed
                inside = vm.stack.pop()
                container = vm.stack.pop()

                # can reuse functions from the interpreter
                result = _evaluate_index_expression(container, inside)
                vm.stack.push(result)
            case opcodes.OPCALL:
                n_arguments = _number_of_function_arguments(vm.instructions, vm.instruction_pointer)
                vm.instruction_pointer += opcodes.OPCALL_WIDTH

                # before calling a function, we put on the stack:
                # - the compiled function object itself
                # - *then* the arguments to that function
                # so we need to take that into account when finding the function's location on the stack
                function_pointer = vm.stack.size() - 1 - n_arguments
                function = vm.stack[function_pointer]
                if not isinstance(function, objs.CompiledFunctionObject):
                    raise VirtualMachineError("Attempted to call a non-function.")

                # we want to return to just after the function (which we will then pop off the
                # stack using OPRETURNVALUE or OPRETURN)
                base_pointer = function_pointer + 1
                frame = StackFrame(function, base_pointer=base_pointer)
                vm.frames.push(frame)

                # reserve `n_locals` entries on the stack for the function's local parameters
                vm.stack.advance_stack_pointer(function.n_locals)
            case opcodes.OPRETURNVALUE:
                # by the end of the function's body, the object we want should be on top of the stack
                return_value = vm.stack.pop()

                # go back to the parent frame
                current_frame = vm.frames.pop()
                n_locals = current_frame.function.n_locals
                vm.stack.shrink_stack_pointer(n_locals)

                # the function we just went through should be right under the returned value; it was
                # sitting there the whole time we moved through the function's body; we want it gone now
                vm.stack.pop()

                # this is replacing the compiled function with the return value we actually want
                vm.stack.push(return_value)
            case opcodes.OPRETURN:
                # a function that ends with an `opcodes.OPRETURN` call doesn't put anything on the
                # stack within its body; so we need to explicitly put NULL on the stack
                current_frame = vm.frames.pop()
                n_locals = current_frame.function.n_locals
                vm.stack.shrink_stack_pointer(n_locals)

                # because nothing is returned, the function we just went through should be on top of the
                # stack; no need to pop off, and then push back on, some kind of returned value
                vm.stack.pop()

                vm.stack.push(objs.NULL_OBJ)
            case _:
                raise VirtualMachineError(f"Could not find a matching opcode: Found: {opcode!r}")


def _evaluate_index_expression(container: objs.Object, inside: objs.Object) -> objs.Object:
    if isinstance(container, objs.ArrayObject) and isinstance(inside, objs.IntegerObject):
        return _evaluate_array_index_expression(container, inside)
    if isinstance(container, objs.StringObject) and isinstance(inside, objs.IntegerObject):
        return _evaluate_string_index_expression(container, inside)
    if isinstance(container, objs.HashObject):
        return _evaluate_hash_index_expression(container, inside)
    else:
        container_str = OBJECT_TYPE_DICT[container.data_type()]
        inside_str = OBJECT_TYPE_DICT[inside.data_type()]
        raise VirtualMachineError(
            "Indexing operation not supported by the compiler.\n"
            f"container type: {container_str}\n"
            f"inside type: {inside_str}\n"
        )


def _evaluate_array_index_expression(array: objs.ArrayObject, index: objs.IntegerObject) -> objs.Object:
    arr_index: int = index.value
    max_allowed: int = len(array.elements) - 1

    if arr_index < 0 or arr_index > max_allowed:
        raise VirtualMachineError(
            "Indexing array out of bounds.\n" f"Array length: {len(array.elements)}\n" f"Index: {index}"
        )

    return array.elements[arr_index]


def _evaluate_string_index_expression(string: objs.StringObject, index: objs.IntegerObject) -> objs.Object:
    str_index: int = index.value
    max_allowed: int = len(string.value) - 1

    if str_index < 0 or str_index > max_allowed:
        raise VirtualMachineError(
            "Indexing string out of bounds.\n" f"String length: {len(string.value)}\n" f"Index: {index}"
        )

    return objs.StringObject(string.value[str_index])


def _evaluate_hash_index_expression(hashmap: objs.HashObject, key: objs.Object) -> objs.Object:
    hashed_key = objs.create_object_hash(key)
    if hashed_key.data_type == objs.ObjectType.ERROR:
        key_str = OBJECT_TYPE_DICT[key.data_type()]
        raise VirtualMachineError("Found an unhashable type as a key in a hashmap.\n" f"key type: {key_str}")

    pair = hashmap.pairs.get(hashed_key, None)
    if pair is None:
        raise VirtualMachineError(f"Key {key} not found in a hash map.")
    else:
        return pair.value


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
    return _read_position(instructions, instr_ptr, opcodes.OPSETGLOBAL_WIDTH)


def _local_identifier_index(instructions: code.Instructions, instr_ptr: int) -> int:
    return _read_position(instructions, instr_ptr, opcodes.OPSETLOCAL_WIDTH)


def _new_position_after_jump(vm: VirtualMachine, instr_ptr: int) -> int:
    jump_position = _read_position(vm.instructions, instr_ptr, opcodes.OPJUMP_WIDTH)
    return jump_position - 1


def _number_of_function_arguments(instructions: code.Instructions, instr_ptr: int) -> int:
    return _read_position(instructions, instr_ptr, opcodes.OPCALL_WIDTH)


def _new_position_after_jump_when_false(vm: VirtualMachine, instr_ptr: int) -> int:
    condition = vm.stack.pop()

    if not objs.is_truthy(condition):
        jump_position = _read_position(vm.instructions, instr_ptr, opcodes.OPJUMPWHENFALSE_WIDTH)
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
    position = _read_position(vm.instructions, instr_ptr, opcodes.OPCONSTANT_WIDTH)
    constant = vm.constants[position]
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


def _read_position(instructions: code.Instructions, instr_ptr: int, operand_width: int) -> int:
    begin_ptr = instr_ptr + 1
    end_ptr = begin_ptr + operand_width
    position_bytes = instructions[begin_ptr:end_ptr]
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
