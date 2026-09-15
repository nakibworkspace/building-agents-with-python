"""
Lesson 04 — Decision making demo.

Run from the agent-builder/ directory:
    python -m lessons.04_decision_making.demo
"""

from my_agent import Agent


def route(intent):
    """Pretend router — in a real agent, each intent maps to a real handler."""
    handlers = {
        "answer_question":  "→ calling Q&A handler",
        "summarize_text":   "→ calling summarizer",
        "translate":        "→ calling translator",
        "none_of_the_above": "→ falling back to general chat",
    }
    return handlers.get(intent, f"→ no handler for {intent!r}")


def main():
    agent = Agent("ollama:llama3.2:latest")

    choices = [
        "answer_question",
        "summarize_text",
        "translate",
        "none_of_the_above",
    ]

    requests = [
        "Can you summarize this article for me?",
        "Translate 'good morning' to French.",
        "What's the capital of Bangladesh?",
        "Tell me about your weekend.",  # none_of_the_above expected
        "Make this short and concise for me.",
        "Summarize this"
    ]

    for req in requests:
        intent = agent.decide(req, choices)
        if intent is None:
            print(f"request: {req!r}  →  DECISION FAILED")
        else:
            print(f"request: {req!r}  →  {intent}  {route(intent)}")
        print()


if __name__ == "__main__":
    main()
