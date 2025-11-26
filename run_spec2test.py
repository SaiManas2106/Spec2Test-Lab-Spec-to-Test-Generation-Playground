from rich.console import Console
from rich.table import Table

from spec2test.tasks import TASKS
from spec2test.model_providers import DummyTestProvider
from spec2test.test_agent import SpecToTestAgent
from spec2test.evaluator import evaluate_agent


def main() -> None:
    console = Console()
    console.print(
        "[bold cyan]Spec2Test Lab – Spec-to-Test Generation Playground[/bold cyan]\n"
    )

    provider = DummyTestProvider()
    agent = SpecToTestAgent(provider)

    results = evaluate_agent(agent, TASKS)

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Task", style="bold")
    table.add_column("Tests OK on canonical?", justify="center")
    table.add_column("Buggy impl", justify="left")
    table.add_column("Tests caught bug?", justify="center")

    for r in results:
        first_row = True
        for bug in r.bug_checks:
            table.add_row(
                r.task_name if first_row else "",
                "✅" if r.tests_ok_on_canonical else "❌",
                bug.impl_label,
                "✅" if bug.tests_failed else "❌",
            )
            first_row = False

    console.print(table)
    console.print(
        "\n[dim]Provider: DummyTestProvider (hand-written tests). "
        "Swap this for a small LLM-based test generator in a thesis setting.[/dim]"
    )


if __name__ == "__main__":
    main()
