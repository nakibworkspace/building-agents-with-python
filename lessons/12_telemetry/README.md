# Lesson 12 — Telemetry (Runtime Observability)

## What question this lesson answers

> "What is my agent actually doing at runtime?"

Evals (L11) tell you if it works *before* deployment. Telemetry tells you what's happening *during* deployment. Without telemetry, debugging is guesswork.

## Concepts you should leave this lesson with

1. **Structured logging, not print statements.** JSON spans on disk. Searchable, parseable.
2. **Spans + traces.** A span = one operation. A trace = one full agent interaction, linked by `trace_id`.
3. **Metrics.** Aggregates you can glance at: success rate, avg latency, retry count.
4. **Start with a file.** Don't reach for OpenTelemetry on day one. A JSONL file is enough.

## What you implement

Nothing — the scaffolding is in `my_agent/telemetry.py`. Three classes:
- `Span` — one operation (`@dataclass`)
- `Metrics` — running counters (`@dataclass` with derived properties)
- `Telemetry` — logs spans to a file, tracks metrics, prints summary

Plus one helper: `timed_llm_call(telemetry, prompt, call_fn, retries)` — wraps a call with timing + logging.

## The flow

```python
agent = Agent("ollama:llama3.2:latest")
telemetry = Telemetry(log_file="agent_telemetry.jsonl")

trace_id = telemetry.start_trace()

# Time an LLM call
response = timed_llm_call(
    telemetry,
    prompt="What is Python?",
    call_fn=lambda p: agent.llm.generate(p),
)

# ... do more work ...

telemetry.end_trace()
telemetry.print_summary()
```

The JSONL log file looks like:
```
{"span_id": "a1b2c3d4", "trace_id": "x9y8z7w6", "event_type": "llm_call", "timestamp": "...", "duration_ms": 1523.45, "data": {"prompt_length": 18, "response_length": 142, "retries": 0}}
```

To debug one interaction:
```bash
grep "x9y8z7w6" agent_telemetry.jsonl
```

## What to log

| Event | Data |
|---|---|
| LLM call | prompt length, response length, duration, success, retries |
| Tool call | tool name, arguments, success, error |
| Memory op | operation (add/get), item |
| Decision | choices, selected |

## Try once it runs

1. Run the demo — see the summary print + JSONL file appear.
2. Open `agent_telemetry.jsonl` — each line is a span.
3. Call `telemetry.log_tool_call(...)` from inside `execute_tool_call()` to wire it up automatically.
4. Read the log file, find a slow call, understand why.

## Output
```bash
Trace ID: e6574470

[1] Generating response...
    -> Python is a high-level, interpreted programming language that is widely used for...

[2] Structured output...
    -> {'answer': '4'}

[3] Tool call...
    -> calculator({'a': 42, 'b': 7, 'operation': 'multiply'}) = 294

[4] Memory op...
    -> memory items: 1

========================================
TELEMETRY SUMMARY
========================================
LLM Calls:   1
  Success Rate: 100.00%
  Avg Latency:  5296ms
  Retries:      0
Tool Calls:  1
  Success Rate: 100.00%
========================================

Spans written to: agent_telemetry.jsonl
```