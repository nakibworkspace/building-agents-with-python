# Lesson 11 — Evals (Regression Testing for Agents)

## What question this lesson answers

> "How do I know my agent still works after I change something?"

Prompts are code. Change a word, and JSON parsing can silently break. An "improvement" can make tool calls less reliable. Without evals, quality degrades silently.

## Concepts you should leave this lesson with

1. **Evals are just assertions.** Run the agent on known inputs, check outputs, report pass/fail.
2. **Golden datasets are your contract.** Version-controlled known-good cases. If they fail, the agent is broken.
3. **Hard assertions first.** "JSON parsed", "required field present", "tool name matches". Save semantic checks for later.
4. **Run before every change.** Make change → run evals → fix or revert → commit.

## What you implement

Nothing — this lesson is mostly glue. The scaffolding is already done.

- `my_agent/evals.py` — `EvalResult`, `EvalSuiteResult`, `AgentEval`, `print_eval_report`
- `evals/golden_datasets.py` — `STRUCTURED_OUTPUT_GOLDEN`, `TOOL_CALL_GOLDEN`, `DECISION_GOLDEN`, `MEMORY_GOLDEN`

## The eval flow

```python
agent = Agent("ollama:llama3.2:latest")
ev = AgentEval(agent)

results = ev.run_all(
    structured_cases=STRUCTURED_OUTPUT_GOLDEN,
    decision_cases=DECISION_GOLDEN,
    tool_cases=TOOL_CALL_GOLDEN,
    memory_cases=MEMORY_GOLDEN,
)

print_eval_report(results)
```

Output looks like:
```
==================================================
EVAL REPORT
==================================================

Structured Output: PASSED (3/3)
Decisions:         PASSED (4/4)
Tool Calls:        PASSED (5/5)
Memory Cycle:      PASSED (3/3)

Overall: ALL PASSED (15/15)
==================================================
```

## Try once it runs

1. Run the demo — should be all green.
2. Open `evals/golden_datasets.py` and add a new structured-output case. Watch the suite run.
3. Intentionally break a prompt in `agent.py` — see the suite catch the regression.
4. Add an edge case (empty input, unicode) to one of the golden datasets.

## Output
```bash
==================================================
EVAL REPORT
==================================================

Structured Output: Structured Output: PASSED (3/3)
Decisions: Decisions: PASSED (4/4)
Tool Calls: Tool Calls: PASSED (5/5)
Memory Cycle: Memory Cycle: FAILED (1/3)
  FAIL: I prefer dark mode
        error: Memory not retrieved
        expected: contains 'dark'
        actual:   I don't have information about your preference for display mode.
  FAIL: I live in New York
        error: Memory not retrieved
        expected: contains 'New York'
        actual:   I don't know where you live.

Overall: 2 FAILED (13/15)
==================================================
```
