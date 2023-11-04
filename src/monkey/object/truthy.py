"""
This module contains a function that determines if a Monkey language Object evaluates
to true or false.
"""

from monkey.object.object import Object
from monkey.object.constants import TRUE_BOOL_OBJ
from monkey.object.constants import FALSE_BOOL_OBJ
from monkey.object.constants import NULL_OBJ


TRUTHY_DICT: dict[Object, bool] = {
    TRUE_BOOL_OBJ: True,
    FALSE_BOOL_OBJ: False,
    NULL_OBJ: False,
}


def is_truthy(obj: Object) -> bool:
    return TRUTHY_DICT.get(obj, True)
