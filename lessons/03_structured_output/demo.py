"""
Lesson 03 — Structured output demo.

Run from the agent-builder/ directory:
    python -m lessons.03_structured_output.demo
"""

from my_agent import Agent


def main():
    agent = Agent("ollama:llama3.2:latest")

    # Schema is a plain string we inject into the prompt.
    # Modern LLMs read this format fine — no need for a real JSON Schema object.
    schema = """
{
  "topic": string,
  "difficulty": "beginner" | "intermediate" | "advanced"
}
"""

    result = agent.generate_structured(
        "Explain quantum computing",
        schema,
    )

    if result is None:
        print("Failed after 3 retries — model couldn't produce valid JSON.")
    else:
        print("Got structured output:")
        print(result)
        print()
        print(f"  topic:      {result.get('topic')}")
        print(f"  difficulty: {result.get('difficulty')}")

    # Run again — temperature=0 should keep this stable
    print("\n--- Second call (should be similar) ---")
    result2 = agent.generate_structured("Explain quantum computing", schema)
    print(result2)


if __name__ == "__main__":
    main()
