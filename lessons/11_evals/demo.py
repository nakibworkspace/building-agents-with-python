"""
Lesson 11 — Evals demo.

Run from the agent-builder/ directory:
    python -m lessons.11_evals.demo
"""

from my_agent import Agent
from my_agent.evals import AgentEval, print_eval_report
from evals.golden_datasets import (
    STRUCTURED_OUTPUT_GOLDEN,
    DECISION_GOLDEN,
    TOOL_CALL_GOLDEN,
    MEMORY_GOLDEN,
)


def main():
    agent = Agent("ollama:llama3.2:latest")
    ev = AgentEval(agent)

    results = ev.run_all(
        structured_cases=STRUCTURED_OUTPUT_GOLDEN,
        decision_cases=DECISION_GOLDEN,
        tool_cases=TOOL_CALL_GOLDEN,
        memory_cases=MEMORY_GOLDEN,
    )

    print_eval_report(results)


if __name__ == "__main__":
    main()
