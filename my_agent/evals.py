"""
Evals — regression testing for the agent.

An eval suite runs the agent on a set of known inputs and asserts
things didn't break. No pytest, no frameworks — just data + assertions.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class EvalResult:
    """Result of a single eval case."""

    passed: bool
    input: Any = None
    expected: Any = None
    actual: Any = None
    error: Optional[str] = None


@dataclass
class EvalSuiteResult:
    """Result of running an entire eval suite."""

    name: str
    passed: int = 0
    failed: int = 0
    results: list[EvalResult] = field(default_factory=list)

    def add_result(self, result: EvalResult) -> None:
        if result.passed:
            self.passed += 1
        else:
            self.failed += 1
        self.results.append(result)

    @property
    def pass_rate(self) -> float:
        total = self.passed + self.failed
        return self.passed / total if total > 0 else 0.0

    def summary(self) -> str:
        status = "PASSED" if self.failed == 0 else "FAILED"
        return f"{self.name}: {status} ({self.passed}/{self.passed + self.failed})"


class AgentEval:
    """Regression testing for agent capabilities.

    Pass your `Agent` instance in. Each `test_*` method returns
    an `EvalSuiteResult` with per-case pass/fail detail.
    """

    def __init__(self, agent):
        self.agent = agent

    # --------------------------------------------------------

    def test_structured_output(self, cases: list[dict]) -> EvalSuiteResult:
        """Run structured-output cases. Checks JSON parsed + required fields present."""
        suite = EvalSuiteResult(name="Structured Output")

        for case in cases:
            result = self.agent.generate_structured(case["input"], case["schema"])

            if result is None:
                suite.add_result(
                    EvalResult(
                        passed=False,
                        input=case["input"],
                        error="Failed to parse JSON",
                    )
                )
                continue

            missing = [f for f in case.get("must_have_fields", []) if f not in result]
            if missing:
                suite.add_result(
                    EvalResult(
                        passed=False,
                        input=case["input"],
                        expected=f"Fields: {case['must_have_fields']}",
                        actual=f"Missing: {missing}",
                        error="Schema contract violated",
                    )
                )
                continue

            suite.add_result(
                EvalResult(passed=True, input=case["input"], actual=result)
            )

        return suite

    # --------------------------------------------------------

    def test_decisions(self, cases: list[dict]) -> EvalSuiteResult:
        """Run decision cases. Checks the chosen option matches `expected`."""
        suite = EvalSuiteResult(name="Decisions")

        for case in cases:
            decision = self.agent.decide(case["input"], case["choices"])

            if decision == case["expected"]:
                suite.add_result(
                    EvalResult(
                        passed=True,
                        input=case["input"],
                        expected=case["expected"],
                        actual=decision,
                    )
                )
            else:
                suite.add_result(
                    EvalResult(
                        passed=False,
                        input=case["input"],
                        expected=case["expected"],
                        actual=decision,
                        error="Wrong routing decision",
                    )
                )

        return suite

    # --------------------------------------------------------

    def test_tool_calls(self, cases: list[dict]) -> EvalSuiteResult:
        """Run tool-call cases. Checks correct tool name + correct args."""
        suite = EvalSuiteResult(name="Tool Calls")

        for case in cases:
            tool_call = self.agent.request_tool(case["input"])

            if tool_call is None:
                suite.add_result(
                    EvalResult(
                        passed=False,
                        input=case["input"],
                        error="No tool call produced",
                    )
                )
                continue

            if tool_call.get("tool") != case["expected_tool"]:
                suite.add_result(
                    EvalResult(
                        passed=False,
                        input=case["input"],
                        expected=case["expected_tool"],
                        actual=tool_call.get("tool"),
                        error="Wrong tool selected",
                    )
                )
                continue

            args = tool_call.get("arguments", {})
            for key, val in case.get("expected_args", {}).items():
                if args.get(key) != val:
                    suite.add_result(
                        EvalResult(
                            passed=False,
                            input=case["input"],
                            expected=case["expected_args"],
                            actual=args,
                            error=f"Wrong arg: {key}",
                        )
                    )
                    break
            else:
                suite.add_result(
                    EvalResult(
                        passed=True,
                        input=case["input"],
                        expected=case["expected_args"],
                        actual=args,
                    )
                )

        return suite

    # --------------------------------------------------------

    def test_memory_cycle(self, cases: list[dict]) -> EvalSuiteResult:
        """Run memory cases. Stores a fact, then queries — checks the fact comes back."""
        suite = EvalSuiteResult(name="Memory Cycle")
        self.agent.memory.clear()

        for case in cases:
            self.agent.run_with_memory(case["store_input"])
            reply = self.agent.run_with_memory(case["query_input"])
            reply_text = (reply or {}).get("reply", "") or ""

            needle = case["expected_in_response"].lower()
            if needle in reply_text.lower():
                suite.add_result(
                    EvalResult(
                        passed=True,
                        input=case["store_input"],
                        actual=reply_text,
                    )
                )
            else:
                suite.add_result(
                    EvalResult(
                        passed=False,
                        input=case["store_input"],
                        expected=f"contains '{case['expected_in_response']}'",
                        actual=reply_text,
                        error="Memory not retrieved",
                    )
                )

        return suite

    # --------------------------------------------------------

    def run_all(
        self,
        structured_cases: Optional[list[dict]] = None,
        decision_cases: Optional[list[dict]] = None,
        tool_cases: Optional[list[dict]] = None,
        memory_cases: Optional[list[dict]] = None,
    ) -> list[EvalSuiteResult]:
        """Run every suite that has cases provided. Returns a list of results."""
        results: list[EvalSuiteResult] = []
        if structured_cases:
            results.append(self.test_structured_output(structured_cases))
        if decision_cases:
            results.append(self.test_decisions(decision_cases))
        if tool_cases:
            results.append(self.test_tool_calls(tool_cases))
        if memory_cases:
            results.append(self.test_memory_cycle(memory_cases))
        return results


def print_eval_report(results: list[EvalSuiteResult]) -> None:
    """Print a human-readable summary of all suite results."""
    print("=" * 50)
    print("EVAL REPORT")
    print("=" * 50)
    print()

    total_passed = 0
    total_failed = 0

    for suite in results:
        print(f"{suite.name}: {suite.summary()}")
        for r in suite.results:
            if not r.passed:
                print(f"  FAIL: {str(r.input)[:60]}")
                print(f"        error: {r.error}")
                if r.expected is not None:
                    print(f"        expected: {r.expected}")
                if r.actual is not None:
                    print(f"        actual:   {r.actual}")
        total_passed += suite.passed
        total_failed += suite.failed

    print()
    total = total_passed + total_failed
    overall = "ALL PASSED" if total_failed == 0 else f"{total_failed} FAILED"
    print(f"Overall: {overall} ({total_passed}/{total})")
    print("=" * 50)
