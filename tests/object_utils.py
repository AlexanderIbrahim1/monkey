from typing import Any

import monkey.object as objs


def is_expected_object(actual: objs.Object, expected_value: Any) -> bool:
    match expected_value:
        case int():
            return is_integer_object(actual, expected_value)
        case _:
            return False


def is_integer_object(actual: objs.Object, expected_value: int) -> bool:
    if not isinstance(actual, objs.IntegerObject):
        return False

    return actual.value == expected_value
