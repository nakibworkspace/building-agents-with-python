"""
Lesson 01 — quick demo.

Run from the agent-builder/ directory:
    python -m lessons.01_basic_chat.demo
or
    python lessons/01_basic_chat/demo.py
"""

from my_agent import Agent


def main():
    agent = Agent("ollama:llama3.2:latest")
    response = agent.simple_generate("Tell me about AI Agents.")
    print("Model said:", response)


if __name__ == "__main__":
    main()
