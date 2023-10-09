"""
This module contains code specific to evaluating instances of BooleanLiteral.
"""

from typing import Callable
from typing import Sequence

import monkey.object as objs
import monkey.parser.expressions as exprs


SequenceEvaluator = Callable[[Sequence[exprs.Expression], objs.Environment], list[objs.Object]]


def evaluate_array_literal(
    node: exprs.ArrayLiteral, seq_eval_fn: SequenceEvaluator, env: objs.Environment
) -> objs.Object:
    elements = seq_eval_fn(node.elements, env)
    if len(elements) == 1 and objs.is_error_object(elements[0]):
        return elements[0]

    return objs.ArrayObject(elements)
