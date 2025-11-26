# Spec2Test Lab – Spec-to-Test Generation Playground

Spec2Test Lab is a small **developer playground** for experimenting with
AI-style **test generation** from simple function specifications.

The idea:

- Define a few small function specs (katas).
- For each spec, an **agent** proposes a set of pytest tests.
- The lab runs those tests against:
  - a **correct** implementation and
  - a couple of intentionally **buggy** implementations,
  and shows which bugs the tests manage to catch.

Right now the project ships with a **DummyTestProvider** that returns
hand-written tests so everything runs locally with no API keys.
In a thesis setting, this provider can be replaced with a real **small,
specialized model** (e.g., a local code model that generates tests from a spec).

This project sits in the *same ecosystem* as a thesis on
“evaluation of AI-driven code and test generation agents”, but it is **not**
a research evaluation framework. It is a lightweight **sandbox** that
demonstrates:

- a clean abstraction for spec-to-test agents,
- automated execution of generated tests,
- the basic idea of “do my tests actually catch bugs?”,
- extensible Python structure suitable for plugging in real models later.
