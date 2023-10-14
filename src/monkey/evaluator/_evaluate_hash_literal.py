"""
This module contains code specific to evaluating instances of HashLiteral.
"""

from typing import Callable

from monkey.parser import ASTNode
import monkey.object as objs
import monkey.parser.expressions as exprs


def evaluate_hash_literal(
    eval_func: Callable[[ASTNode], objs.Object], node: exprs.HashLiteral
) -> objs.Object:
    hash_pairs: dict[objs.ObjectHash, objs.HashKeyValuePair] = {}

    for key_expr, value_expr in node.key_value_pairs:
        key = eval_func(key_expr)
        if objs.is_error_object(key):
            return key

        object_hash = objs.create_object_hash(key)
        if object_hash.data_type == objs.ObjectType.ERROR:
            return objs.UnhashableTypeErrorObject(key.data_type())

        value = eval_func(value_expr)
        if objs.is_error_object(value):
            return value

        hash_pairs[object_hash] = objs.HashKeyValuePair(key, value)

    return objs.HashObject(hash_pairs)
