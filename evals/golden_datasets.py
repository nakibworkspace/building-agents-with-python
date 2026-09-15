"""
Golden datasets for agent evals.

A "golden" case is a known-good example that must always pass.
If a golden case fails, the agent is broken — not the test.

Keep these small. 5-10 cases per capability is plenty to start.
Add more as you find edge cases in production.
"""


# ============================================================
# STRUCTURED OUTPUT
# Tests: JSON parsing + schema compliance
# ============================================================

STRUCTURED_OUTPUT_GOLDEN = [
    {
        "input": "Explain quantum computing in one sentence",
        "schema": """{
  "topic": "the topic name as a string",
  "difficulty": "beginner" or "intermediate" or "advanced"
}

Example: {"topic": "machine learning", "difficulty": "intermediate"}""",
        "must_have_fields": ["topic", "difficulty"],
    },
    {
        "input": "What is Python in one sentence?",
        "schema": """{
  "topic": "the topic name as a string",
  "difficulty": "beginner" or "intermediate" or "advanced"
}

Example: {"topic": "web development", "difficulty": "beginner"}""",
        "must_have_fields": ["topic", "difficulty"],
    },
    {
        "input": "What is the significance of 42?",
        "schema": """{
  "answer": "your answer as a string"
}

Example: {"answer": "It is the meaning of life"}""",
        "must_have_fields": ["answer"],
    },
]


# ============================================================
# TOOL CALLS
# Tests: correct tool selection + valid arguments
# ============================================================

TOOL_CALL_GOLDEN = [
    {
        "input": "What is 42 * 7?",
        "expected_tool": "calculator",
        "expected_args": {"operation": "multiply"},
    },
    {
        "input": "Calculate 100 + 50",
        "expected_tool": "calculator",
        "expected_args": {"operation": "add"},
    },
    {
        "input": "What is 100 / 5?",
        "expected_tool": "calculator",
        "expected_args": {"operation": "divide"},
    },
    {
        "input": "What's 50 minus 25?",
        "expected_tool": "calculator",
        "expected_args": {"operation": "subtract"},
    },
    {
        "input": "If I have 15 apples and buy 27 more, how many do I have?",
        "expected_tool": "calculator",
        "expected_args": {"operation": "add"},
    },
]


# ============================================================
# DECISIONS
# Tests: correct routing based on input
# ============================================================

DECISION_GOLDEN = [
    {
        "input": "Can you summarize this article for me?",
        "choices": ["answer_question", "summarize_text", "translate"],
        "expected": "summarize_text",
    },
    {
        "input": "Translate 'hello' to Spanish",
        "choices": ["answer_question", "summarize_text", "translate"],
        "expected": "translate",
    },
    {
        "input": "What is the capital of France?",
        "choices": ["answer_question", "summarize_text", "translate"],
        "expected": "answer_question",
    },
    {
        "input": "What is 5 + 5?",
        "choices": ["answer_question", "calculate", "search"],
        "expected": "calculate",
    },
]


# ============================================================
# MEMORY
# Tests: store -> retrieve cycle
# ============================================================

MEMORY_GOLDEN = [
    {
        "store_input": "My name is Alice",
        "query_input": "What's my name?",
        "expected_in_response": "Alice",
    },
    {
        "store_input": "I prefer dark mode",
        "query_input": "What's my preference for display mode?",
        "expected_in_response": "dark",
    },
    {
        "store_input": "I live in New York",
        "query_input": "Where do I live?",
        "expected_in_response": "New York",
    },
]
