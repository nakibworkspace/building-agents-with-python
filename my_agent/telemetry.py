"""
Telemetry — runtime observability for the agent.

Three primitives:
  - Span:  one operation (one LLM call, one tool execution)
  - Trace: a group of spans linked by trace_id (one agent interaction)
  - Metrics: aggregate counters (success rate, latency, retries)

We write spans to a JSONL file. Plain text on disk. No frameworks.
"""

import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class Span:
    """One operation in a trace."""

    span_id: str
    trace_id: str
    event_type: str
    timestamp: str
    duration_ms: Optional[float] = None
    data: Optional[dict] = None
    error: Optional[str] = None


@dataclass
class Metrics:
    """Running counters for the agent."""

    llm_calls: int = 0
    llm_failures: int = 0
    llm_retries: int = 0
    tool_calls: int = 0
    tool_failures: int = 0
    total_latency_ms: float = 0.0

    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / self.llm_calls if self.llm_calls > 0 else 0.0

    @property
    def llm_success_rate(self) -> float:
        return 1 - (self.llm_failures / self.llm_calls) if self.llm_calls > 0 else 0.0

    @property
    def tool_success_rate(self) -> float:
        return 1 - (self.tool_failures / self.tool_calls) if self.tool_calls > 0 else 0.0


class Telemetry:
    """Simple file-based telemetry."""

    def __init__(self, log_file: str = "agent_telemetry.jsonl"):
        self.log_file = log_file
        self.current_trace_id: Optional[str] = None
        self.metrics = Metrics()

    # ----- trace lifecycle --------------------------------------------------

    def start_trace(self) -> str:
        """Begin a new trace. Returns the trace_id."""
        self.current_trace_id = str(uuid4())[:8]
        return self.current_trace_id

    def end_trace(self) -> None:
        """End the current trace."""
        self.current_trace_id = None

    # ----- logging ---------------------------------------------------------

    def _write_span(self, span: Span) -> None:
        with open(self.log_file, "a") as f:
            f.write(json.dumps(asdict(span)) + "\n")

    def log_llm_call(
        self,
        prompt_length: int,
        response_length: int,
        duration_ms: float,
        success: bool = True,
        error: Optional[str] = None,
        retries: int = 0,
    ) -> None:
        span = Span(
            span_id=str(uuid4())[:8],
            trace_id=self.current_trace_id or "no-trace",
            event_type="llm_call",
            timestamp=datetime.now().isoformat(),
            duration_ms=round(duration_ms, 2),
            data={
                "prompt_length": prompt_length,
                "response_length": response_length,
                "retries": retries,
            },
            error=error,
        )
        self._write_span(span)

        self.metrics.llm_calls += 1
        self.metrics.total_latency_ms += duration_ms
        self.metrics.llm_retries += retries
        if not success:
            self.metrics.llm_failures += 1

    def log_tool_call(
        self,
        tool_name: str,
        arguments: dict,
        duration_ms: float = 0.0,
        success: bool = True,
        error: Optional[str] = None,
    ) -> None:
        span = Span(
            span_id=str(uuid4())[:8],
            trace_id=self.current_trace_id or "no-trace",
            event_type="tool_call",
            timestamp=datetime.now().isoformat(),
            duration_ms=round(duration_ms, 4),
            data={"tool": tool_name, "arguments": arguments},
            error=error,
        )
        self._write_span(span)

        self.metrics.tool_calls += 1
        if not success:
            self.metrics.tool_failures += 1

    def log_memory_op(
        self, operation: str, item: Optional[str] = None
    ) -> None:
        span = Span(
            span_id=str(uuid4())[:8],
            trace_id=self.current_trace_id or "no-trace",
            event_type="memory_op",
            timestamp=datetime.now().isoformat(),
            data={"operation": operation, "item": item},
        )
        self._write_span(span)

    def log_decision(self, choices: list, selected: Optional[str]) -> None:
        span = Span(
            span_id=str(uuid4())[:8],
            trace_id=self.current_trace_id or "no-trace",
            event_type="decision",
            timestamp=datetime.now().isoformat(),
            data={"choices": choices, "selected": selected},
        )
        self._write_span(span)

    # ----- reporting -------------------------------------------------------

    def print_summary(self) -> None:
        """Print a human-readable metrics summary."""
        m = self.metrics
        print("=" * 40)
        print("TELEMETRY SUMMARY")
        print("=" * 40)
        print(f"LLM Calls:   {m.llm_calls}")
        print(f"  Success Rate: {m.llm_success_rate * 100:.2f}%")
        print(f"  Avg Latency:  {m.avg_latency_ms:.0f}ms")
        print(f"  Retries:      {m.llm_retries}")
        print(f"Tool Calls:  {m.tool_calls}")
        print(f"  Success Rate: {m.tool_success_rate * 100:.2f}%")
        print("=" * 40)


# Convenience: a context manager-ish helper for timing LLM calls.
def timed_llm_call(telemetry: Telemetry, prompt: str, call_fn, retries: int = 0):
    """Time a single LLM call, log it, return the result.

    `call_fn(prompt)` should return the raw response string.
    """
    start = time.time()
    try:
        response = call_fn(prompt)
        duration = (time.time() - start) * 1000
        telemetry.log_llm_call(
            prompt_length=len(prompt),
            response_length=len(response or ""),
            duration_ms=duration,
            success=True,
            retries=retries,
        )
        return response
    except Exception as e:
        duration = (time.time() - start) * 1000
        telemetry.log_llm_call(
            prompt_length=len(prompt),
            response_length=0,
            duration_ms=duration,
            success=False,
            error=str(e),
            retries=retries,
        )
        raise