"""
This module contains mnemonics for all the operating codes used in this compiler for
the monkey language.

NOTE: I can't name this module `opcode.py` because it causes the black formatting tool
to break when run in this directory.
"""

from monkey.code.code import Opcode


OPCONSTANT: Opcode = b"0"
OPPOP: Opcode = b"1"
OPADD: Opcode = b"2"
OPSUB: Opcode = b"3"
OPMUL: Opcode = b"4"
OPDIV: Opcode = b"5"

OPCONSTANT_WIDTH: int = 2
