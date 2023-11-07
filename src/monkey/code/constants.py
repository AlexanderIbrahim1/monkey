"""
This module contains constants that could be used in other areas of the project.
"""

# number of bytes used to describe position of address
ADDRESS_POSITION_SIZE: int = 2

# number of bytes used to describe the number assigned to a binding
BINDING_BYTE_SIZE: int = 2

# the maximum allowed address
MAXIMUM_ADDRESS: int = 2 ** (8 * ADDRESS_POSITION_SIZE) - 1

# an address equal to the maximum allowed address, used as a temporary dummy value
DUMMY_ADDRESS: int = MAXIMUM_ADDRESS

# maximum number of digits an address can take in base 10
MAXIMUM_ADDRESS_DIGITS: int = len(str(MAXIMUM_ADDRESS))
