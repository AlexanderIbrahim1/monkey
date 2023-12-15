"""
This module contains custom types used in the `code` package, that might be used
in other locations at well.
"""

from monkey.code.code import Opcode

Operands = tuple[int, ...]
OpcodeOperandPair = tuple[Opcode, Operands]
