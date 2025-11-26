````markdown
# Spec2Test Lab – Spec-to-Test Generation Playground

Spec2Test Lab is a small Python playground for **spec-driven test generation**.  
It takes simple function specifications, uses an agent to turn them into pytest suites, and runs those tests against both **correct** and **buggy** implementations to show where tests catch or miss bugs. The design makes it easy to later plug in **small LLM-based test generators** instead of the dummy provider.

## Features

- `TestTask` objects with:
  - natural-language spec,
  - function name,
  - canonical implementation,
  - multiple buggy implementations.
- `DummyTestProvider`:
  - returns hand-written pytest tests (no external APIs needed).
- `SpecToTestAgent`:
  - wraps a provider and generates tests for each task.
- Evaluation pipeline:
  - tests must pass on the canonical implementation,
  - tests are run against buggy implementations to see which bugs are caught.
- Rich CLI output:
  - table view of each task and buggy implementation, with ✅/❌ status.

## Project structure

```text
spec2test_lab/
  README.md
  requirements.txt
  run_spec2test.py        # CLI entrypoint

  spec2test/
    __init__.py
    tasks.py              # TestTask definitions + implementations
    model_providers.py    # BaseTestProvider + DummyTestProvider
    test_agent.py         # SpecToTestAgent
    evaluator.py          # Evaluation logic

  tests/
    test_pipeline_smoke.py
````

## Getting started

From the project root:

```bash
# 1. Create and activate virtual environment
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the playground
python run_spec2test.py
```

You’ll see a table showing, for each task:

* whether tests pass on the canonical implementation, and
* for each buggy implementation, whether the tests caught the bug.

## Extending

* Add new tasks in `spec2test/tasks.py` with more specs and buggy implementations.
* Implement a new provider in `spec2test/model_providers.py` that calls a small LLM or other test generator.
* Use the existing evaluator as a base for deeper experiments with **AI-assisted testing**.
