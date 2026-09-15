"""
Lesson 02 — System prompt demo.

Run from the agent-builder/ directory:
    python -m lessons.02_system_prompt.demo
"""

from my_agent import Agent


def main():
    agent = Agent("ollama:llama3.2:latest")

    question = "Explain what an API is."

    # L01: no role
    raw = agent.simple_generate(question)
    print("--- simple_generate (no role) ---")
    print(raw)
    print()

    # L02: with role (uses agent's default system_prompt)
    with_role = agent.generate_with_role(question)
    print("--- generate_with_role (default persona) ---")
    print(with_role)
    print()

    # L02: swap the persona mid-session
    agent.system_prompt = "You are a 5-year-old explaining things to a friend. Use simple words and short sentences."
    playful = agent.generate_with_role(question)
    print("--- generate_with_role (5-year-old persona) ---")
    print(playful)


if __name__ == "__main__":
    main()
