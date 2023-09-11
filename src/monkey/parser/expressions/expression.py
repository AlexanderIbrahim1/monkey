"""
This module contains the Expression abstract class, which indicates that the node
in the AST is an expression (produces a value).
"""

from abc import ABC
from abc import abstractmethod

from monkey.parser.ast_node import ASTNode


class Expression(ASTNode, ABC):
    @abstractmethod
    def expression_node(self) -> None:
        """
        A dummy function, causing the Python static analysis tools to throw errors when
        we use a type that implements `ASTNode` as a `Expression`, but it isn't a `Expression`.
        """
