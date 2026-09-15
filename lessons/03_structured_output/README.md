# Lesson 03 — Structured Output (JSON contracts)

## What question this lesson answers

> "How do I stop parsing free-text?"

Free-text responses are probabilistic. Sometimes the model adds prose, sometimes it forgets a comma, sometimes it just refuses. You can't build anything reliable on top of that. **Structured output is a contract** — you tell the model exactly what shape to return, and you validate it before you trust it.

## Concepts you should leave this lesson with

1. **The contract is a string in the prompt.** Tell the model the JSON shape you want. Llama 3.2 reads schemas reasonably well.
2. **`temperature=0.0`** reduces randomness. Doesn't make outputs deterministic, just more consistent.
3. **Retries turn probability into reliability.** One attempt fails ~10–20% of the time. Three attempts almost always succeed.
4. **Validation is non-negotiable.** Never trust `response.choices[0].message.content` without parsing it first.

## What you implement

```python
generate_structured(self, user_input, schema) -> dict | None
```

Returns a parsed dict, or `None` if 3 attempts all fail.

## Why this lesson is the inflection point

L01, L02 produced text. L03 produces **data**. Everything after this — decisions (L04), tools (L05), loops (L06), memory (L07), planning (L08) — is built on the assumption that you can get structured data out of the model. This is that lesson.

## Try these once it runs

1. Pass a schema for a book (`title`, `author`, `year`, `genre`). Ask "Recommend a sci-fi book." What fields does the model fill?
2. Run the same call 5 times — is the output stable? Should be more stable than L01.
3. Run with a deliberately vague schema (`{"stuff": "..."}`) — does the model still produce useful output?
4. Force a failure: ask for a number but request JSON with a list. Watch the retries.

## Output
```bash
Got structured output:
{'topic': 'quantum computing', 'difficulty': 'advanced'}

  topic:      quantum computing
  difficulty: advanced

--- Second call (should be similar) ---
{'topic': 'quantum computing', 'difficulty': 'advanced'}
```
