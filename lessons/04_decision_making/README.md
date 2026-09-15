# Lesson 04 — Decision Making

## What question this lesson answers

> "Can the model **decide** what to do, not just answer?"

L03 had the model **generate** values for a schema. L04 has it **select** from a fixed list. Selection is fundamentally more constrained than generation — there's only ever N valid outputs, so:

- Hallucination of new actions is impossible
- You can validate membership in O(1)
- You can route on the result with a simple `if/elif` chain

## Concepts you should leave this lesson with

1. **Generation vs selection** — L03 generates new values; L04 picks from your list. Both are valid, selection is more reliable when the option set is known.
2. **Validation against the source list** — never trust `parsed["decision"]` until you've checked it's actually in `choices`. The model can pick *almost* the right word.
3. **You are the routing layer** — after the decision comes back as a string, your code decides what to do with it. The model doesn't "act" — it "decides", and you act.
4. **Decision schemas are action spaces** — these choices ARE the agent's possible behaviors. Keep them small, distinct, and unambiguous.

## What you implement

```python
decide(self, user_input, choices) -> str | None
```

Returns one of `choices`, or `None` if all retries fail to produce a valid member.

## Why this matters

Every agent framework under the hood has a "decision" step somewhere. LangGraph calls it a router. LangChain agents call it tool selection. AutoGen calls it speaker selection. **They're all L04**: "give the model N options, get back a selection."

## Try these once it runs

1. Run the same `user_input` 5 times — does the choice stay consistent at `temperature=0.0`?
2. Add a `"none_of_the_above"` choice — when does the model pick it?
3. Make two choices semantically close (`"summarize"` vs `"tldr"`) — does it confuse them?
4. Pass an empty list — what should happen? What's the safe behavior?

## What's next

Lesson 05 — Tool Calling. Same idea as L04 (the model picks), but instead of naming a *concept* it specifies *what function to call and with what arguments*. That's the moment your agent starts having **effects** on the world.
