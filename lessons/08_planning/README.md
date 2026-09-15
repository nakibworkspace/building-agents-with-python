# Lesson 08 — Planning (data, not thoughts)

## What question this lesson answers

> "How does the agent decompose a goal before acting?"

Up to now, the agent reacts step-by-step. L08 has it **plan first**: turn a goal into an ordered list of steps, then execute them. **The plan is inspectable data**, not hidden chain-of-thought.

## Concepts you should leave this lesson with

1. **Plans are data.** `{"steps": ["do X", "then Y", "then Z"]}` — a Python dict you can print, modify, save.
2. **Generate then execute is two stages.** First ask the model for the plan. Then run each step. You can edit the plan between stages.
3. **Plans are not magic.** They're just the same LLM call you've written 5 times, with a different JSON shape.
4. **Naive execution is fine for now.** This lesson's `execute_plan()` just records that each step ran. Real execution comes in L09.

## What you implement

```python
create_plan(self, goal) -> dict | None        # YOU write this (1 line!)
execute_plan(self, plan) -> list               # already written for you
```

`create_plan` is a one-liner that calls the helper in `planner.py`. The interesting logic lives in the helper, not the wrapper.

## The flow

```
goal                                  "Explain how HTTPS works"
   │
   ▼
create_plan(goal)
   │
   ▼
planner.create_plan(llm, goal)        # builds prompt, asks LLM, validates
   │
   ▼
{"steps": [
   "Define what HTTPS stands for",
   "Explain the TLS handshake",
   "Describe certificate validation",
   "Compare to HTTP"
]}
   │
   ▼
execute_plan(plan)                    # records each step
   │
   ▼
[{"step": "Define...", "executed": True}, ...]
```

## Why this is in `planner.py`

Same reason `Memory` is in `memory.py` and `tools.py` has tools: small focused modules. The planner has zero state — it's a pure function over (llm, goal) → dict. Easy to test in isolation later.

## Try these once it runs

1. Goal = "Plan a birthday party" — see how granular the steps get
2. Goal = "Add 5 + 3" — does the model over-plan (5 steps) or keep it minimal (1)?
3. Goal = "" (empty string) — what happens? Should fail cleanly.
4. Inspect the plan dict between stages — you can edit it before executing.

## Output
```bash
=== Goal: Explain how HTTPS works to a beginner ===
Plan:
  1. Step 1: Introduction to HTTPS
  2. Step 2: How HTTPS Works
  3. Step 3: Benefits of HTTPS
  4. Step 4: How to Implement HTTPS
  5. Step 5: Common HTTPS Scenarios
  6. Step 6: Troubleshooting HTTPS Issues

Executed 6 steps. State steps: 6

=== Goal: Plan a small birthday party for a 7-year-old ===
Plan:
  1. Plan guest list
  2. Send out invitations
  3. Prepare party games
  4. Order party food
  5. Decorate party area
  6. Prepare party favors
  7. Set up party schedule
  8. Have party
  9. Clean up after party

Executed 9 steps. State steps: 15

=== Goal: Compare Python and JavaScript for a new programmer ===
Plan:
  1. Step 1: Learn the basics of both languages
  2. Step 2: Choose a project to work on
  3. Step 3: Compare the syntax and features of both languages
  4. Step 4: Evaluate the ecosystem and community support for each language
  5. Step 5: Consider the job prospects and salary ranges for each language
  6. Step 6: Make an informed decision based on the comparison and chosen project

Executed 6 steps. State steps: 21
```
