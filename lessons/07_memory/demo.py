"""
Lesson 07 — Memory demo.

Run from the agent-builder/ directory:
    python -m lessons.07_memory.demo
"""

from my_agent import Agent


def chat(agent, message):
    """One conversation turn."""
    result = agent.run_with_memory(message)
    if result is None:
        return "(no response)"
    reply = result.get("reply", "")
    saved = result.get("save_to_memory")
    if saved:
        print(f"   [saved: {saved!r}]")
    return reply


def main():
    agent = Agent("ollama:llama3.2:latest")

    print("Turn 1: introduce yourself")
    print(f"> Alice: Hi, my name is Alice and I'm a Python developer.")
    print(f"< Agent: {chat(agent, 'Hi, my name is Alice and I am a Python developer.')}")
    print()

    print(f"\nMemory after turn 1: {agent.memory.get_all()}\n")

    print("Turn 2: ask the agent to recall")
    print("> Alice: What is my name?")
    print(f"< Agent: {chat(agent, 'What is my name?')}")
    print()

    print("Turn 3: ask the agent to recall profession")
    print("> Alice: What do I do for work?")
    print(f"< Agent: {chat(agent, 'What do I do for work?')}")
    print()

    print(f"\nFinal memory: {agent.memory.get_all()}")


if __name__ == "__main__":
    main()
