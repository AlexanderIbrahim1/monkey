"""
This module contains the FixedStack class, which is an implementation of a stack
with a fixed size in Python.

I could technically just use a list, whose size is limited essentially just by the
system's available memory. But because this is a pedagogical project, I want to include
the effects of having a maximum stack size.
"""

from typing import Callable
from typing import Generic
from typing import Optional
from typing import TypeVar

T = TypeVar("T")


class FixedStackError(Exception):
    pass


class FixedStack(Generic[T]):
    def __init__(self, max_size: int, default_element_factory: Optional[Callable[[], T]] = None) -> None:
        self._data: list[T] = []
        self._max_size = max_size
        self._stack_pointer = 0
        self._default_element_factory = default_element_factory

    def push(self, element: T) -> None:
        if self._stack_pointer == self._max_size:
            raise FixedStackError(
                f"Attempted to push an element beyond the stack's size limit of {self._max_size}"
            )

        if len(self._data) <= self._stack_pointer:
            self._data.append(element)
        else:
            self._data[self._stack_pointer] = element

        self._stack_pointer += 1

    def pop(self) -> T:
        if self._stack_pointer == 0:
            raise FixedStackError("Attempted to pop an empty stack.")

        element = self._data[self._stack_pointer - 1]
        self._stack_pointer -= 1

        return element

    def maybe_pop(self) -> Optional[T]:
        if self._stack_pointer == 0:
            return None

        element = self._data[self._stack_pointer - 1]
        self._stack_pointer -= 1

        return element

    def peek(self) -> T:
        if self._stack_pointer == 0:
            raise FixedStackError("Attempted to peek at the top of an empty stack.")

        return self._data[self._stack_pointer - 1]

    def maybe_peek(self) -> Optional[T]:
        if self._stack_pointer == 0:
            return None

        return self._data[self._stack_pointer - 1]

    def __getitem__(self, index: int) -> T:
        if not (0 <= index < self._stack_pointer):
            raise FixedStackError("Attempted to access element out of bounds of the stack.")

        return self._data[index]

    def __setitem__(self, index: int, value: T) -> None:
        if not (0 <= index < self._stack_pointer):
            raise FixedStackError("Attempted to write element out of bounds of the stack.")

        self._data[index] = value

    def maybe_get(self, index: int) -> Optional[T]:
        if not (0 <= index < self._stack_pointer):
            return None

        return self._data[index]

    def maybe_get_last_popped(self) -> Optional[T]:
        if len(self._data) <= self._stack_pointer:
            return None

        return self._data[self._stack_pointer]

    def size(self) -> int:
        return self._stack_pointer

    def is_empty(self) -> bool:
        return self.size() == 0

    def shrink_stack_pointer(self, n_elements: int) -> None:
        if n_elements < 0:
            raise FixedStackError(
                "Must provide a positive value to shrink the stack pointer by.\n" f"Provided: {n_elements}"
            )

        new_stack_pointer = self._stack_pointer - n_elements
        if new_stack_pointer < 0:
            raise FixedStackError(
                "Cannot shrink the stack pointer below 0\n"
                f"Current: {self._stack_pointer}\n"
                f"Proposed shrink: {n_elements}"
            )

        self._stack_pointer = new_stack_pointer

    def advance_stack_pointer(self, n_elements: int) -> None:
        if n_elements < 0:
            raise FixedStackError(
                "Must provide a positive value to advance the stack pointer by.\n" f"Provided: {n_elements}"
            )

        new_stack_pointer = self._stack_pointer + n_elements

        if new_stack_pointer > self._max_size:
            raise FixedStackError(
                f"Cannot advance the stack pointer above the maximum size of {self._max_size}.\n"
                f"Current: {self._stack_pointer}\n"
                f"Proposed shrink: {n_elements}"
            )

        # checking the edge case: `self._stack_pointer` always points to the element ahead of
        # the number of elements in the stack; i.e. the index of where the next element will be
        # - if the stack is empty, `self._stack_pointer == 0`
        # - if the stack has 1 element, `self._stack_pointer == 1`
        # ...
        # so the new stack pointer is only an issue if it is greater than the inner data's length
        if new_stack_pointer > len(self._data):
            if self._default_element_factory is None:
                raise FixedStackError(
                    "Attempted to advance the stack pointer past the size of the\n"
                    "wrapped list, but no default element factory has been set."
                )

            while len(self._data) < new_stack_pointer:
                new_element = self._default_element_factory()
                self._data.append(new_element)

        self._stack_pointer = new_stack_pointer
