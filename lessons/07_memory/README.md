# Lesson 07 — Memory

## What question this lesson answers

> "How does the agent remember things across turns?"

Until now, each call to the agent was **stateless** — no awareness of past conversations. Memory gives the agent a place to **store facts** and a way to **inject them into future prompts**.

## Concepts you should leave this lesson with

1. **Memory is data, not consciousness.** It's just a Python list of strings. No neural net, no retrieval embeddings, no magic.
2. **The agent decides what to remember.** The model returns a `save_to_memory` field for any fact worth keeping. Your code stores it.
3. **Memory is injected into the prompt.** Each turn starts with "Here are your memories:" so the model can use them.
4. **Memory has limits.** No dedup-by-meaning, no time-decay. That's fine for a basic implementation — and you can extend later.

## What you implement

```python
run_with_memory(self, user_input) -> dict | None   # YOU write this
```

One method. It does three things:
1. Build prompt with memory context + the user's input
2. Ask the model for `{"reply": "...", "save_to_memory": "..."}`
3. If `save_to_memory` is set, `self.memory.add(...)` it. Return the parsed dict.

## Try these once it runs

1. Tell the agent "My name is Alice." Then ask "What's my name?" — it should answer "Alice" from memory.
2. Tell the agent "I'm a Python developer." Then ask "What do I do?" — recall.
3. Print `agent.memory.get_all()` after each turn — see what's being remembered.
4. Clear memory mid-session: `agent.memory.clear()`. Does the agent forget?

## What's next

Lesson 08 — Planning. Instead of one step at a time, the agent first generates a **plan** (ordered list of steps), then executes them. Plans are inspectable data, not hidden chain-of-thought.
