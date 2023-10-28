"""
This module contains code specific to evaluating instances of BooleanLiteral.
"""

import monkey.object as objs
import monkey.parser.expressions as exprs

from monkey.tokens.reserved_identifiers import TRUE_IDENTIFIER


def evaluate_boolean_literal(node: exprs.BooleanLiteral) -> objs.Object:
    if node.value == TRUE_IDENTIFIER:
        return objs.TRUE_BOOL_OBJ
    else:
        return objs.FALSE_BOOL_OBJ
