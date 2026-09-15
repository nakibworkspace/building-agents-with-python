# Lesson 10 — Atom of Thought (AoT)

## What question this lesson answers

> "How do you represent a plan where some actions depend on others — and might run in parallel?"

L08 produced a **flat ordered list**. L10 produces a **graph**: each node is an atomic action, and `depends_on` declares which nodes must finish first.

## Concepts you should leave this lesson with

1. **Plans aren't always linear.** "Research X" and "Research Y" can run in parallel. "Write summary" must wait for both.
2. **Dependencies are data.** `depends_on: ["1"]` means "I cannot run until node 1 finishes." The executor just respects this.
3. **Topological execution is simple.** Keep iterating until every node is done, picking nodes whose deps are satisfied.
4. **AoT ≠ DAG orchestration frameworks.** Airflow, Prefect, LangGraph — all build on this same idea with extra features (retries, persistence, UI).

## What you implement

```python
create_aot_plan(self, goal) -> dict | None       # YOU write this (1 line)
execute_aot_plan(self, graph) -> list            # already written for you
```

`create_aot_plan` is a one-line wrapper, same as L08/L09. `execute_aot_plan` delegates to `planner.execute_graph()`, which I wrote — it does the topological loop.

## The structure

```python
graph = {
    "nodes": [
        {"id": "1", "action": "research_X", "depends_on": []},
        {"id": "2", "action": "research_Y", "depends_on": []},   # parallel with 1
        {"id": "3", "action": "compare",    "depends_on": ["1", "2"]},  # waits for both
        {"id": "4", "action": "summarize",  "depends_on": ["3"]},
    ]
}
```

The executor walks the graph, executing any node whose deps are all done. Marks each as `executed` after running.

## Why this is the "real" planning

L08 was "list of steps in order". L10 captures the actual **structure of work**:
- Parallelism: independent steps run concurrently (in theory)
- Ordering: dependent steps wait
- Inspection: you can `print(graph)` and see the full topology

## Try these once it runs

1. Generate a graph for "Write a blog post about AI agents" — see if the model naturally identifies parallel vs sequential work.
2. Manually edit the graph: add a fake dependency or remove one. Watch the executor fail/succeed accordingly.
3. Try a goal where the model **doesn't** produce good dependencies — see the failure mode.
4. Look at `execute_graph()` in `planner.py` — it's ~25 lines, no magic.

## Output
```bash
=== Goal: Write a short blog post comparing Python and JavaScript ===
Graph nodes:
  [1] research  depends_on=[]
  [2] choose  depends_on=['1']
  [3] write  depends_on=['2']
  [4] review  depends_on=['3']
  [5] edit  depends_on=['4']
  [6] publish  depends_on=['5']

Executed 6 nodes:
  ✓ [1] research  →  Executed: research
  ✓ [2] choose  →  Executed: choose
  ✓ [3] write  →  Executed: write
  ✓ [4] review  →  Executed: review
  ✓ [5] edit  →  Executed: edit
  ✓ [6] publish  →  Executed: publish

=== Goal: Plan a healthy weekly meal prep ===
Graph nodes:
  [1] plan  depends_on=[]
  [2] research  depends_on=['1']
  [3] make  depends_on=['2']
  [4] shop  depends_on=['3']
  [5] cook  depends_on=['4']
  [6] review  depends_on=['5']

Executed 6 nodes:
  ✓ [1] plan  →  Executed: plan
  ✓ [2] research  →  Executed: research
  ✓ [3] make  →  Executed: make
  ✓ [4] shop  →  Executed: shop
  ✓ [5] cook  →  Executed: cook
  ✓ [6] review  →  Executed: review
```
