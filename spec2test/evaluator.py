import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from typing import List

from .tasks import TestTask
from .test_agent import SpecToTestAgent, GeneratedTests


@dataclass
class BugCheckResult:
    impl_label: str
    tests_failed: bool  # True if tests failed against this impl (i.e., bug was caught)


@dataclass
class TaskEvaluation:
    task_name: str
    tests_ok_on_canonical: bool
    bug_checks: List[BugCheckResult]


def _write_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _run_pytest(test_file: str, cwd: str) -> bool:
    """Run pytest on the given file; return True if exit code is 0 (all tests pass)."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", test_file],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def evaluate_task(agent: SpecToTestAgent, task: TestTask) -> TaskEvaluation:
    generated: GeneratedTests = agent.generate_for_task(task)

    bug_checks: List[BugCheckResult] = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # 1) Check tests against canonical impl (should pass)
        impl_correct_path = os.path.join(tmpdir, "impl_under_test.py")
        tests_path = os.path.join(tmpdir, "test_generated.py")

        _write_file(impl_correct_path, task.canonical_impl)
        _write_file(tests_path, generated.tests_source)

        tests_ok_on_canonical = _run_pytest("test_generated.py", cwd=tmpdir)

        # 2) Check tests against each buggy impl (we hope they fail)
        for idx, buggy_impl in enumerate(task.buggy_impls, start=1):
            impl_buggy_path = os.path.join(tmpdir, "impl_under_test.py")
            _write_file(impl_buggy_path, buggy_impl)
            tests_passed = _run_pytest("test_generated.py", cwd=tmpdir)
            bug_checks.append(
                BugCheckResult(
                    impl_label=f"buggy_{idx}",
                    tests_failed=not tests_passed,
                )
            )

    return TaskEvaluation(
        task_name=task.name,
        tests_ok_on_canonical=tests_ok_on_canonical,
        bug_checks=bug_checks,
    )


def evaluate_agent(agent: SpecToTestAgent, tasks: List[TestTask]) -> List[TaskEvaluation]:
    return [evaluate_task(agent, t) for t in tasks]
