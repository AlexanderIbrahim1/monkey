"""
This module contains the definitions needed to work with the bytecode for the
monkey language compiler
"""

from typing import Annotated

# NOTE:
# - the book says that it is easier ot work with a `bytes`-like type directly, instead of
#   creating a specific type for an Instruction; this is to cut down on the type-casting;
# - I'm not sure if the same concerns would hold up in Python, but I'll follow their advice

Instructions = bytes
Opcode = Annotated[bytes, "length of 1"]
