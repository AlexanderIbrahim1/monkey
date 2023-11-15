from typing import Any

import monkey.object as objs


def is_expected_object(actual: objs.Object, expected_value: Any) -> bool:
    match expected_value:
        case bool():
            return is_boolean_object(actual, expected_value)
        case int():
            return is_integer_object(actual, expected_value)
        case str():
            return is_string_object(actual, expected_value)
        case None:
            return is_null_object(actual)
        case list():
            return is_list_object(actual, expected_value)
        case _:
            return False


def is_list_object(actual: objs.Object, expected_value: list[Any]) -> bool:
    if not isinstance(actual, objs.ArrayObject):
        return False

    return all(
        [
            is_expected_object(actual_element, expected_element)
            for (actual_element, expected_element) in zip(actual.elements, expected_value)
        ]
    )


def is_integer_object(actual: objs.Object, expected_value: int) -> bool:
    if not isinstance(actual, objs.IntegerObject):
        return False

    return actual.value == expected_value


def is_string_object(actual: objs.Object, expected_value: str) -> bool:
    if not isinstance(actual, objs.StringObject):
        return False

    return actual.value == expected_value


def is_boolean_object(actual: objs.Object, expected_value: bool) -> bool:
    if not isinstance(actual, objs.BooleanObject):
        return False

    return actual.value == expected_value


def is_null_object(actual: objs.Object) -> bool:
    return isinstance(actual, objs.NullObject)
