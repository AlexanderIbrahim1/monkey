"""
This module contains constants relevant to the functioning of the VirtualMachine, that
are used by other modules in this subpackage.
"""

MAX_VM_STACK_SIZE: int = 2048
MAX_VM_GLOBALS_SIZE: int = 2048
MAX_VM_FRAME_SIZE: int = 2048

# the VM creates the main function when creating the 0th stack frame; it needs a field
# set for the number of locals, but this doesn't (currently) make sense because it is
# in the global scope
#
# the book doesn't address this, and because the book uses Go, I assume it just leaves
# the number of locals undefined (to the point that I've read, page 200)
#
# I need a dummy value to keep mypy and pyright quiet
DUMMY_MAIN_FUNCTION_NUMBER_OF_LOCALS: int = -1
