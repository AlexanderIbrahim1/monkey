"""
This module contains code specific to evaluating instances of InfixExpression.
"""

import monkey.object as objs


def evaluate_index_expression(container: objs.Object, inside: objs.Object) -> objs.Object:
    if isinstance(container, objs.ArrayObject) and isinstance(inside, objs.IntegerObject):
        return _evaluate_array_index_expression(container, inside)
    else:
        return objs.InvalidIndexingErrorObject(container.data_type(), inside.data_type())


def _evaluate_array_index_expression(array: objs.ArrayObject, index: objs.IntegerObject) -> objs.Object:
    arr_index: int = index.value
    max_allowed: int = len(array.elements) - 1

    if arr_index < 0 or arr_index > max_allowed:
        return objs.OutOfBoundsErrorObject(array.data_type(), arr_index, len(array.elements))

    return array.elements[arr_index]
