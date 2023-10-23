import pytest

from monkey.containers import FixedStack
from monkey.containers import FixedStackError


class TestFixedStack:
    def test_basic(self):
        stack = FixedStack[int](10)

        assert stack.is_empty()

        stack.push(5)

        assert stack.size() == 1
        assert stack.pop() == 5
        assert stack.is_empty()

    def test_stack_with_zero_size(self):
        stack = FixedStack[int](0)
        assert stack.size() == 0
        assert stack.is_empty()

    def test_size_after_construction(self):
        stack = FixedStack[int](10)
        assert stack.size() == 0

    def test_size_after_push(self):
        stack = FixedStack[int](10)
        stack.push(1)
        stack.push(2)
        stack.push(3)

        assert stack.size() == 3

    def test_raises_push_past_max(self):
        stack = FixedStack[int](3)
        stack.push(1)
        stack.push(2)
        stack.push(3)

        with pytest.raises(FixedStackError):
            stack.push(10)

    def test_size_decreases_with_popping(self):
        stack = FixedStack[int](10)
        for _ in range(3):
            stack.push(0)

        assert stack.size() == 3
        stack.pop()
        assert stack.size() == 2
        stack.pop()
        assert stack.size() == 1
        stack.pop()
        assert stack.size() == 0

    def test_values_from_popping(self):
        stack = FixedStack[int](10)

        stack.push(1)
        stack.push(2)
        stack.push(3)
        assert stack.pop() == 3
        assert stack.pop() == 2
        assert stack.pop() == 1

    def test_raises_pop_empty_stack(self):
        stack = FixedStack[int](10)

        stack.push(1)
        stack.pop()

        with pytest.raises(FixedStackError):
            stack.pop()

    def test_raises_pop_empty_stack_just_after_construction(self):
        stack = FixedStack[int](10)
        with pytest.raises(FixedStackError):
            stack.pop()

    @pytest.mark.parametrize("values", [(1, 2, 3), (1, 2), (1,)])
    def test_peek_value(self, values):
        stack = FixedStack[int](10)

        for v in values:
            stack.push(v)

        assert stack.peek() == values[-1]

    def test_peek_does_not_modify_size(self):
        stack = FixedStack[int](10)
        stack.push(10)
        assert stack.size() == 1
        assert stack.peek() == 10
        assert stack.size() == 1

    def test_raises_peek_empty_stack(self):
        stack = FixedStack[int](10)

        stack.push(1)
        stack.pop()

        with pytest.raises(FixedStackError):
            stack.peek()

    def test_raises_peek_empty_stack_just_after_construction(self):
        stack = FixedStack[int](10)
        with pytest.raises(FixedStackError):
            stack.peek()

    @pytest.mark.parametrize("n_times_to_push_and_pop", [0, 1, 5])
    def test_is_empty(self, n_times_to_push_and_pop):
        stack = FixedStack[int](100)

        for _ in range(n_times_to_push_and_pop):
            stack.push(1)
            stack.pop()

        assert stack.is_empty()

    @pytest.mark.parametrize("n_elements", [1, 2, 5])
    def test_is_not_empty(self, n_elements):
        stack = FixedStack[int](100)

        for _ in range(n_elements):
            stack.push(1)

        assert not stack.is_empty()

    @pytest.mark.parametrize("n_elements", [0, 1, 2, 5])
    def test_size(self, n_elements):
        stack = FixedStack[int](100)

        for _ in range(n_elements):
            stack.push(1)

        assert stack.size() == n_elements

    def test_getitem(self):
        stack = FixedStack[int](3)
        stack.push(1)
        stack.push(2)
        stack.push(3)

        assert stack[0] == 1
        assert stack[1] == 2
        assert stack[2] == 3

    def test_raises_getitem_out_of_bounds(self):
        stack = FixedStack[int](3)
        stack.push(1)
        with pytest.raises(FixedStackError):
            stack[2]

    @pytest.mark.parametrize("index", [-1, 0, 1, 2])
    def test_raises_getitem_on_empty_stack(self, index: int):
        stack = FixedStack[int](10)
        with pytest.raises(FixedStackError):
            stack[index]

    def test_values_from_maybe_pop(self):
        stack = FixedStack[int](10)

        stack.push(1)
        stack.push(2)
        stack.push(3)
        assert stack.maybe_pop() == 3
        assert stack.maybe_pop() == 2
        assert stack.maybe_pop() == 1

    def test_maybe_pop_empty_stack(self):
        stack = FixedStack[int](10)

        stack.push(1)
        stack.pop()
        assert stack.maybe_pop() is None

    @pytest.mark.parametrize("values", [(1, 2, 3), (1, 2), (1,)])
    def test_maybe_peek_value(self, values):
        stack = FixedStack[int](10)

        for v in values:
            stack.push(v)

        assert stack.maybe_peek() == values[-1]

    def test_maybe_peek_empty_stack(self):
        stack = FixedStack[int](10)

        stack.push(1)
        stack.pop()
        assert stack.maybe_peek() is None

    def test_maybe_get(self):
        stack = FixedStack[int](3)
        stack.push(1)
        stack.push(2)
        stack.push(3)

        assert stack.maybe_get(0) == 1
        assert stack.maybe_get(1) == 2
        assert stack.maybe_get(2) == 3

    def test_maybe_get_out_of_bounds(self):
        stack = FixedStack[int](3)
        stack.push(1)
        assert stack.maybe_get(2) is None

    @pytest.mark.parametrize("elements", [(1,), (1, 2), (1, 2, 3)])
    def test_maybe_get_last_popped(self, elements):
        stack = FixedStack[int](3)

        for elem in elements:
            stack.push(elem)

        stack.pop()

        assert stack.maybe_get_last_popped() == elements[-1]

    def test_empty_maybe_get_last_popped(self):
        stack = FixedStack[int](3)
        assert stack.maybe_get_last_popped() is None
