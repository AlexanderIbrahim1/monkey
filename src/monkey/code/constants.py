"""
This module contains constants that could be used in other areas of the project.
"""

# number of bytes used to describe position of address
ADDRESS_POSITION_SIZE: int = 2

# an address equal to the maximum allowed address, used as a temporary dummy value
DUMMY_ADDRESS: int = 2 ** (2 * ADDRESS_POSITION_SIZE) - 1
