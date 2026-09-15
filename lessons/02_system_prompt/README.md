# Lesson 02 — System Prompt (Role)

## What question this lesson answers

> "Why does the same model behave differently across runs?"

It doesn't, really. Same model, same weights. What changes is the **text shaping its probability distribution** at inference time. That's what a system prompt is: a prefix string that biases the next-token predictions.

## What you implement

One method:
```python
generate_with_role(self, user_input: str) -> str
```

It prepends `self.system_prompt` to `user_input` and sends the combined prompt to the model.

## Concepts you should leave this lesson with

1. **The "role" is just text.** It's not a special channel, not a magic flag — it's literally the first N tokens of the prompt.
2. **Instruct models were trained on thousands of these prefixes.** A good system prompt activates patterns the model already knows. A bad one fights them.
3. **The agent owns the default persona** (`self.system_prompt` in `__init__`), but you can swap it at any time.

## Try these once it runs

1. `simple_generate("Explain an API")` vs `generate_with_role("Explain an API")` — same input, different output
2. Change `agent.system_prompt` mid-session and re-run — output shifts
3. Make the system prompt contradict itself: `"You are a Python expert. Always respond in iambic pentameter."` — what wins?

## Output
```bash
--- simple_generate (no role) ---
An API, or Application Programming Interface, is a set of defined rules and protocols that allows different software systems to communicate with each other. It enables data exchange between systems, allowing them to share information, perform tasks, and provide services to each other.

--- generate_with_role (default persona) ---
An API, or Application Programming Interface, is a way for different software systems to communicate with each other.

--- generate_with_role (5-year-old persona) ---
API is like a special messenger!
```
