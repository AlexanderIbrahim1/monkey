"""
This module contains the AstNode abstract class, which each node in the AST must
implement.
"""

from abc import ABC
from abc import abstractmethod

from monkey.tokens import Literal


class ASTNode(ABC):
    @abstractmethod
    def token_literal(self) -> Literal:
        """Returns the literal value of the token for this node."""
