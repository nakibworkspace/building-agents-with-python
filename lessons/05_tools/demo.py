"""
Lesson 05 — Tool calling demo.

Run from the agent-builder/ directory:
    python -m lessons.05_tools.demo
"""

from my_agent import Agent


def main():
    agent = Agent("ollama:llama3.2:latest")

    questions = [
        "What is 42 times 7?",
        "Add 100 and 200.",
        "Subtract 50 from 1000.",
        "Divide 144 by 12.",
        "What's the capital of France?",  # no tool expected
    ]

    for q in questions:
        print(f"Q: {q}")
        tool_call = agent.request_tool(q)

        if tool_call is None:
            print("  → No tool requested (model answered directly or failed)")
        else:
            print(f"  → requested: {tool_call}")
            try:
                result = agent.execute_tool_call(tool_call)
                print(f"  → result:    {result}")
            except Exception as e:
                print(f"  → tool error: {e}")
        print()


if __name__ == "__main__":
    main()
