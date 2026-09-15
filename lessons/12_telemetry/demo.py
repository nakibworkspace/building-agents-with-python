"""
Lesson 12 — Telemetry demo.

Run from the agent-builder/ directory:
    python -m lessons.12_telemetry.demo
"""

import time

from my_agent import Agent
from my_agent.telemetry import Telemetry, timed_llm_call


def main():
    agent = Agent("ollama:llama3.2:latest")
    telemetry = Telemetry(log_file="agent_telemetry.jsonl")

    # Start a trace — one full agent interaction
    trace_id = telemetry.start_trace()
    print(f"Trace ID: {trace_id}")
    print()

    # 1) LLM call — timed + logged
    print("[1] Generating response...")
    response = timed_llm_call(
        telemetry,
        prompt="What is Python in one sentence?",
        call_fn=lambda p: agent.llm.generate(p),
    )
    print(f"    -> {response[:80]}...")
    print()

    # 2) Structured output — also wrapped
    print("[2] Structured output...")
    structured = agent.generate_structured(
        "What is 2+2?",
        '{"answer": "your answer as a string"}',
    )
    print(f"    -> {structured}")
    print()

    # 3) Tool call — log manually
    print("[3] Tool call...")
    start = time.time()
    tool_call = agent.request_tool("What is 42 * 7?")
    duration = (time.time() - start) * 1000

    if tool_call:
        result = agent.execute_tool_call(tool_call)
        telemetry.log_tool_call(
            tool_name=tool_call["tool"],
            arguments=tool_call["arguments"],
            duration_ms=duration,
            success=True,
        )
        print(f"    -> {tool_call['tool']}({tool_call['arguments']}) = {result}")
    else:
        telemetry.log_tool_call(
            tool_name="calculator",
            arguments={},
            duration_ms=duration,
            success=False,
            error="No tool call produced",
        )
        print("    -> (no tool call)")
    print()

    # 4) Memory operation
    print("[4] Memory op...")
    agent.memory.add("User likes Python")
    telemetry.log_memory_op(operation="add", item="User likes Python")
    print(f"    -> memory items: {len(agent.memory)}")
    print()

    # End trace + report
    telemetry.end_trace()
    telemetry.print_summary()
    print()
    print(f"Spans written to: {telemetry.log_file}")


if __name__ == "__main__":
    main()