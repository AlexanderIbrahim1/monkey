"""
This module contains code specific to evaluating instances of StringLiteral.
"""

import monkey.object as objs
import monkey.parser.expressions as exprs


def evaluate_string_literal(node: exprs.StringLiteral) -> objs.Object:
    return objs.StringObject(node.value)
