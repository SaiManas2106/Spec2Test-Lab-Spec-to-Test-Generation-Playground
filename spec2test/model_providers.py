from abc import ABC, abstractmethod

from .tasks import TestTask


class BaseTestProvider(ABC):
    """Abstract provider that generates pytest tests from a task spec."""

    @abstractmethod
    def generate_tests(self, task: TestTask) -> str:
        """Return Python source code with pytest tests for the given task.

        The tests should import the function under test as:

            from impl_under_test import <function_name>
        """
        raise NotImplementedError


class DummyTestProvider(BaseTestProvider):
    """Simple provider that returns hand-written tests.

    This makes the lab runnable without any external AI services.
    A thesis could replace this with a real small model.
    """

    def generate_tests(self, task: TestTask) -> str:
        if task.name == "sum_positives":
            return self._tests_sum_positives()
        if task.name == "is_palindrome":
            return self._tests_is_palindrome()
        # Fallback: very generic placeholder
        return f"""\
import pytest
from impl_under_test import {task.function_name}


def test_placeholder():
    # Placeholder test – should be replaced by a real provider.
    assert callable({task.function_name})
"""

    def _tests_sum_positives(self) -> str:
        return """\
import pytest
from impl_under_test import sum_positives


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([], 0),
        ([1, 2, 3], 6),
        ([-1, -2, -3], 0),
        ([-1, 0, 4, 5], 9),
        ([0, 1, -2, 3, -4], 4),
    ],
)
def test_sum_positives_basic(nums, expected):
    assert sum_positives(nums) == expected


def test_sum_positives_large_values():
    data = [1000, -5, 2000, 0, -1]
    assert sum_positives(data) == 3000


def test_sum_positives_edge_cases():
    assert sum_positives([0, 0, 0]) == 0
    assert sum_positives([-1]) == 0
"""

    def _tests_is_palindrome(self) -> str:
        return """\
import pytest
from impl_under_test import is_palindrome


@pytest.mark.parametrize(
    "s, expected",
    [
        ("", True),
        ("a", True),
        ("abba", True),
        ("abc", False),
        ("RaceCar", True),
        ("nurses run", True),
        ("not a palindrome", False),
    ],
)
def test_is_palindrome_cases_and_spaces(s, expected):
    assert is_palindrome(s) == expected


def test_is_palindrome_tricky_spacing():
    assert is_palindrome(" r a c e c a r ")
"""
