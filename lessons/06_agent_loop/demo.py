"""
Lesson 06 — Agent loop demo.

Run from the agent-builder/ directory:
    python -m lessons.06_agent_loop.demo
"""

from my_agent import Agent


def main():
    agent = Agent("ollama:llama3.2:latest")

    goal = "Help me understand how recursion works"
    print(f"Goal: {goal}\n")

    results = agent.run_loop(goal, max_steps=3)

    for i, step in enumerate(results, 1):
        action = step.get("action", "?")
        reason = step.get("reason", "(no reason)")
        print(f"Step {i}: {action}")
        print(f"   reason: {reason}")
        print()

    print(f"Total steps taken: {agent.state.steps}")
    print(f"Marked done?       {agent.state.done}")


if __name__ == "__main__":
    main()
