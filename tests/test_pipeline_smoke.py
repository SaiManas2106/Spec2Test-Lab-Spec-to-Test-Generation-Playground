from spec2test.tasks import TASKS
from spec2test.model_providers import DummyTestProvider
from spec2test.test_agent import SpecToTestAgent
from spec2test.evaluator import evaluate_agent


def test_pipeline_runs():
    provider = DummyTestProvider()
    agent = SpecToTestAgent(provider)
    results = evaluate_agent(agent, TASKS)

    assert len(results) == len(TASKS)
    for r in results:
        assert r.task_name in {t.name for t in TASKS}
