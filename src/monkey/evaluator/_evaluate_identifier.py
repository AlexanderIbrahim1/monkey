"""
This module contains code specific to evaluating instances of Identifier.
"""

import monkey.object as objs
import monkey.parser.expressions as exprs

from monkey.evaluator.monkey_builtins import BUILTINS_DICT


def evaluate_identifier(node: exprs.Identifier, env: objs.Environment) -> objs.Object:
    ident_obj = env.get(node.value)
    if not objs.is_error_object(ident_obj):
        return ident_obj

    error_obj = ident_obj

    builtin_obj = BUILTINS_DICT.get(node.value, None)
    if builtin_obj is not None:
        return builtin_obj

    return error_obj
