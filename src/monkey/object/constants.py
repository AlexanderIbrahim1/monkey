"""
Some Object instances have a very limited range of values that they are able to hold,
and it makes sense to simply define some global constants that get repeatedly reused,
instead of creating a new instance of those Objects each time.
"""

from monkey.object.null_object import NullObject
from monkey.object.boolean_object import BooleanObject


NULL_OBJ = NullObject()
TRUE_BOOL_OBJ = BooleanObject(True)
FALSE_BOOL_OBJ = BooleanObject(False)
