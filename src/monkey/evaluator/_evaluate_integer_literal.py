"""
This module contains code specific to evaluating instances of IntegerLiteral.
"""

import monkey.object as objs
import monkey.parser.expressions as exprs


def evaluate_integer_literal(node: exprs.IntegerLiteral) -> objs.Object:
    return objs.IntegerObject(int(node.value))
