"""
This module contains the AstNode abstract class, which each node in the AST must
implement.
"""

from abc import ABC
from abc import abstractmethod
from typing import Any

from monkey.tokens import Literal


class ASTNode(ABC):
    @abstractmethod
    def token_literal(self) -> Literal:
        """Returns the literal value of the token for this node."""

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass
