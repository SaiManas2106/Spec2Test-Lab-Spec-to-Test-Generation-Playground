from dataclasses import dataclass

from .tasks import TestTask
from .model_providers import BaseTestProvider


@dataclass
class GeneratedTests:
    """Container for generated tests for a single task."""

    tests_source: str


class SpecToTestAgent:
    """Agent that generates tests from a specification, via a provider."""

    def __init__(self, provider: BaseTestProvider) -> None:
        self.provider = provider

    def generate_for_task(self, task: TestTask) -> GeneratedTests:
        tests = self.provider.generate_tests(task)
        return GeneratedTests(tests_source=tests)
