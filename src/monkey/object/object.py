"""
This module contains the Object abstract class, which wraps around the values that
come about when we evaluate the AST.
"""

from abc import ABC
from abc import abstractmethod
from typing import Any

from monkey.object.object_type import ObjectType


class Object(ABC):
    @abstractmethod
    def data_type(self) -> ObjectType:
        """Returns the type of object that this Object wraps."""

    @abstractmethod
    def inspect(self) -> str:
        """A tool to inspect the underlying value."""

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """"""

    @abstractmethod
    def __repr__(self) -> str:
        """"""
