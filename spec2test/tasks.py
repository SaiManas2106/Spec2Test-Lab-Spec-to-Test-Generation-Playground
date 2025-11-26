from dataclasses import dataclass
from typing import List


@dataclass
class TestTask:
    """Represents a spec-driven testing kata.

    Each task has:
    - a natural-language description,
    - a function name to implement,
    - one canonical implementation,
    - one or more buggy implementations (to see if tests catch them).
    """
    name: str
    description: str
    function_name: str
    canonical_impl: str
    buggy_impls: List[str]


# --- Task 1: sum_positives ----------------------------------------------------

_SUM_POSITIVES_SPEC = (
    "Given a list of integers, return the sum of all strictly positive values. "
    "Zeros and negative numbers must be ignored."
)

# Outer string uses '''...''' so inner function can use """...""" safely
_SUM_POSITIVES_CANONICAL = '''
def sum_positives(nums: list[int]) -> int:
    """Return the sum of strictly positive integers in the input list."""
    return sum(n for n in nums if n > 0)
'''

# Buggy version 1: off-by-one, ignores the last element in the list
_SUM_POSITIVES_BUGGY_1 = '''
def sum_positives(nums: list[int]) -> int:
    """Buggy implementation: ignores the last element in the list."""
    total = 0
    for i in range(len(nums) - 1):
        if nums[i] > 0:
            total += nums[i]
    return total
'''

# Buggy version 2: counts zeros as positive
_SUM_POSITIVES_BUGGY_2 = '''
def sum_positives(nums: list[int]) -> int:
    """Buggy implementation: treats zero as positive as well."""
    total = 0
    for n in nums:
        if n >= 0:
            total += n
    return total
'''


# --- Task 2: is_palindrome ----------------------------------------------------

_IS_PALINDROME_SPEC = (
    "Return True if a string is a palindrome, ignoring case and whitespace. "
    "Non-space characters must be compared case-insensitively."
)

_IS_PALINDROME_CANONICAL = '''
def is_palindrome(s: str) -> bool:
    """Return True if s is a palindrome, ignoring case and spaces."""
    cleaned = "".join(ch.lower() for ch in s if not ch.isspace())
    return cleaned == cleaned[::-1]
'''

# Buggy 1: case-sensitive and space-sensitive
_IS_PALINDROME_BUGGY_1 = '''
def is_palindrome(s: str) -> bool:
    """Buggy implementation: case-sensitive and space-sensitive."""
    return s == s[::-1]
'''

# Buggy 2: mishandles odd-length strings and whitespace
_IS_PALINDROME_BUGGY_2 = '''
def is_palindrome(s: str) -> bool:
    """Buggy: mishandles odd-length strings and whitespace."""
    s = s.replace(" ", "")
    n = len(s)
    return s[: n // 2] == s[: n // 2 : -1]
'''


TASKS: List[TestTask] = [
    TestTask(
        name="sum_positives",
        description=_SUM_POSITIVES_SPEC,
        function_name="sum_positives",
        canonical_impl=_SUM_POSITIVES_CANONICAL,
        buggy_impls=[_SUM_POSITIVES_BUGGY_1, _SUM_POSITIVES_BUGGY_2],
    ),
    TestTask(
        name="is_palindrome",
        description=_IS_PALINDROME_SPEC,
        function_name="is_palindrome",
        canonical_impl=_IS_PALINDROME_CANONICAL,
        buggy_impls=[_IS_PALINDROME_BUGGY_1, _IS_PALINDROME_BUGGY_2],
    ),
]
