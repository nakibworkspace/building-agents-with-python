"""
Lesson 08 — Planning demo.

Run from the agent-builder/ directory:
    python -m lessons.08_planning.demo
"""

from my_agent import Agent


def main():
    agent = Agent("ollama:llama3.2:latest")

    goals = [
        "Explain how HTTPS works to a beginner",
        "Plan a small birthday party for a 7-year-old",
        "Compare Python and JavaScript for a new programmer",
    ]

    for goal in goals:
        print(f"=== Goal: {goal} ===")
        plan = agent.create_plan(goal)
        if plan is None:
            print("  (no plan generated)\n")
            continue

        print("Plan:")
        for i, step in enumerate(plan.get("steps", []), 1):
            print(f"  {i}. {step}")
        print()

        results = agent.execute_plan(plan)
        print(f"Executed {len(results)} steps. State steps: {agent.state.steps}\n")


if __name__ == "__main__":
    main()
