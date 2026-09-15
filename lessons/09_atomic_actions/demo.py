"""
Lesson 09 — Atomic actions demo.

Run from the agent-builder/ directory:
    python -m lessons.09_atomic_actions.demo
"""

from my_agent import Agent


def main():
    agent = Agent("ollama:llama3.2:latest")

    steps = [
        "Define what HTTPS stands for",
        "Explain the TLS handshake in simple terms",
        "Compare HTTPS to HTTP for a beginner",
        "Write a one-paragraph summary",
    ]

    for step in steps:
        print(f"Step: {step!r}")
        atomic = agent.create_atomic_action(step)
        if atomic is None:
            print("  (decomposition failed)\n")
            continue
        print(f"  action: {atomic.get('action')}")
        print(f"  inputs: {atomic.get('inputs')}")
        print()


if __name__ == "__main__":
    main()
