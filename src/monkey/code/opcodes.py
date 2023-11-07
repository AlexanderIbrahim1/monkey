"""
This module contains mnemonics for all the operating codes used in this compiler for
the monkey language.

NOTE: I can't name this module `opcode.py` because it causes the black formatting tool
to break when run in this directory.
"""

from monkey.code.code import Opcode
from monkey.code.constants import ADDRESS_POSITION_SIZE
from monkey.code.constants import BINDING_BYTE_SIZE


OPCONSTANT: Opcode = b"\x00"
OPPOP: Opcode = b"\x01"
OPADD: Opcode = b"\x02"
OPSUB: Opcode = b"\x03"
OPMUL: Opcode = b"\x04"
OPDIV: Opcode = b"\x05"
OPTRUE: Opcode = b"\x06"
OPFALSE: Opcode = b"\x07"
OPEQUAL: Opcode = b"\x08"
OPNOTEQUAL: Opcode = b"\x09"
OPGREATERTHAN: Opcode = b"\x10"
OPMINUS: Opcode = b"\x11"
OPBANG: Opcode = b"\x12"
OPJUMP: Opcode = b"\x13"
OPJUMPWHENFALSE: Opcode = b"\x14"
OPNULL: Opcode = b"\x15"
OPSETGLOBAL: Opcode = b"\x16"
OPGETGLOBAL: Opcode = b"\x17"

# a dummy opcode used in situations where an opcode instance needs to exist
OPDUMMY: Opcode = b"\xFF"

OPCONSTANT_WIDTH: int = ADDRESS_POSITION_SIZE
OPSETGLOBAL_WIDTH: int = BINDING_BYTE_SIZE
OPGETGLOBAL_WIDTH: int = BINDING_BYTE_SIZE
OPJUMP_WIDTH: int = ADDRESS_POSITION_SIZE
OPJUMPWHENFALSE_WIDTH: int = ADDRESS_POSITION_SIZE
