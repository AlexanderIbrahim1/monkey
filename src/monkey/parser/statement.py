"""
This module contains the Statement abstract class, which indicates that the node
in the AST is a statement (produces no value).
"""

from abc import ABC
from abc import abstractmethod

from monkey.parser.ast_node import ASTNode


class Statement(ASTNode, ABC):
    @abstractmethod
    def statement_node(self) -> None:
        """
        A dummy function, causing the Python static analysis tools to throw errors when
        we use a type that implements `ASTNode` as a `Statement`, but it isn't a `Statement`.
        """
