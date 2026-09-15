# Lesson 06 — The Agent Loop

## What question this lesson answers

> "How does this become an agent and not a chatbot?"

Answer: when it can **observe, decide, act, and repeat** with state.

L01–L05 are components. L06 is the **loop** that ties them together:

```
┌──────────────────────────────────┐
│                                  │
│   observe  ──→  decide  ──→  act │──┐
│                                  │  │
└──────────────────────────────────┘  │
              ↑                      │
              └──────────────────────┘
                  repeat until done
```

## Concepts you should leave this lesson with

1. **An agent is a loop, not a clever prompt.** The "intelligence" comes from repetition + state, not from one big call.
2. **State is explicit.** `self.state.steps`, `self.state.done`. Not hidden in conversation history. You can inspect it any time.
3. **Termination is mandatory.** Without `max_steps` and a `"done"` action, the loop runs forever (or until your bill arrives).
4. **One step = one decision.** Each call to `agent_step()` asks the model "what next?", the loop decides when to stop.

## What you implement

```python
agent_step(self, user_input) -> dict | None     # TODO — you write this
run_loop(self, user_input, max_steps=5) -> list  # already written for you
```

`run_loop()` is the orchestrator — it calls `agent_step()` repeatedly until the agent signals `done` or hits `max_steps`. **You only write the per-step logic.**

## The state machine

```
        ┌──────────┐
   ┌──→ │ steps=0  │ ─── agent_step() ──→ step 1: action="analyze"
   │    └──────────┘                                   │
   │                                                    ▼
   │    ┌──────────┐                              results.append(step)
   │    │ steps=1  │ ─── agent_step() ──→ step 2: action="research"
   │    └──────────┘                                   │
   │                                                    ▼
   │    ...                                             │
   │                                                    ▼
   │    ┌──────────┐                              step N: action="done"
   │    │ steps=N  │ ─── agent_step() ──→ state.mark_done() ──→ exit loop
   │    └──────────┘
```

## Try these once it runs

1. Run `run_loop("Explain loops in programming", max_steps=3)` — see what sequence of actions the model picks
2. Set `max_steps=1` — agent gets one shot, then stops
3. Inspect `agent.state.steps` and `agent.state.done` after a run — verify they're correct
4. Ask a question that requires multiple actions ("Compare X and Y") — does the model plan or just answer?

## What's next

Lessons 07–10 add **memory** (what the agent remembers across turns), **planning** (decompose goals into steps), **atomic actions** (smallest executable units), and **AoT** (Atom of Thought dependency graphs). All of them are just **patterns on top of this loop**.
