# Lesson 09 — Atomic Actions

## What question this lesson answers

> "What does it look like to break a step into something safely executable?"

A plan step like *"Define what HTTPS stands for"* is a **sentence**. To actually execute it, you need it in a form a machine can act on: a verb (`define_term`) + parameters (`{"term": "HTTPS", "definition_kind": "expansion"}`).

That's an **atomic action** — the smallest possible executable unit.

## Concepts you should leave this lesson with

1. **Atomic = smallest unit.** Not "summarize the paper" — too vague. "write_paragraph" with `{"topic": "..."}` is atomic.
2. **Action name = verb.** `write_paragraph`, `lookup_definition`, `compare_items`. Nouns alone (`summary`) are weaker because they don't say what to *do*.
3. **Inputs is a typed dict.** Each action knows what params it expects. Your code can route on the action name + validate inputs.
4. **Atomic ≠ implemented.** This lesson just **generates** atomic specs. Wiring them to real tools is the next step (or out of scope for this repo).

## What you implement

```python
create_atomic_action(self, step) -> dict | None   # YOU write this (1 line)
```

Same pattern as L08: thin wrapper that delegates to `planner.create_atomic_action()`.

## The flow

```
plan step                          "Define what HTTPS stands for"
   │
   ▼
planner.create_atomic_action(llm, step)
   │
   ▼
{"action": "define_term",
 "inputs": {"term": "HTTPS", "definition_kind": "expansion"}}
   │
   ▼
print(action)                       # inspect — you can edit before running
```

## Try these once it runs

1. Take a plan from L08, decompose each step, see how the model reframes natural language into (verb, params).
2. Edit an atomic action by hand: `action["inputs"]["extra_context"] = "for beginners"` — execute it (mock).
3. Try a deliberately vague step: `"do the thing"` — does the model produce a sensible action or hallucinate?
4. Compare two models: small vs larger models sometimes produce very different action vocabularies.

## Output
```bash
Step: 'Define what HTTPS stands for'
  action: define_https
  inputs: {'definition': 'Hypertext Transfer Protocol Secure'}

Step: 'Explain the TLS handshake in simple terms'
  action: explain_tls_handshake
  inputs: {'key': 'simple explanation of the TLS handshake process'}

Step: 'Compare HTTPS to HTTP for a beginner'
  action: compare_https_to_http
  inputs: {'title': 'Comparison of HTTPS to HTTP for a Beginner'}

Step: 'Write a one-paragraph summary'
  action: summary
  inputs: {'text': 'Write a one-paragraph summary'}
```
