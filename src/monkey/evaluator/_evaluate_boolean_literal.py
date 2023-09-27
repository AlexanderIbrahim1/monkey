"""
This module contains code specific to evaluating instances of BooleanLiteral.
"""

import monkey.object as objs
import monkey.parser.expressions as exprs


def evaluate_boolean_literal(node: exprs.BooleanLiteral) -> objs.Object:
    if node.value == "true":
        return objs.TRUE_BOOL_OBJ
    else:
        return objs.FALSE_BOOL_OBJ
