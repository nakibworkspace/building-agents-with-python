# Lesson 05 — Tool Calling

## What question this lesson answers

> "Can the model **ask me** to do something?"

L04 had the model pick from a list of *concepts* (`"summarize_text"`). L05 has it pick a **function** + **arguments** and the agent actually **runs** it. That's the moment your agent has effects on the world.

## Concepts you should leave this lesson with

1. **Tools are APIs you expose, not abilities the model has.** The model doesn't compute — it specifies. Your code computes.
2. **The tool spec is the contract.** You write the schema once, the model reads it from the prompt, the dispatcher validates against it.
3. **Request ≠ Execute.** `request_tool()` returns a *description* of what to run. `execute_tool_call()` is what actually runs it. **Never** let the model trigger execution directly.
4. **Tools extend capability without retraining.** Add a new tool = add a Python function + update the schema. The model learns it from the prompt.

## What you implement

Two methods:

```python
request_tool(self, user_input) -> dict | None       # TODO — you write this
execute_tool_call(self, tool_call) -> Any           # already written for you
```

The first asks the model "which tool, with what args?". The second dispatches.

## The flow

```
user_input                "What is 42 * 7?"
   │
   ▼
request_tool(prompt)      →  {"tool": "calculator",
                               "arguments": {"a": 42, "b": 7,
                                              "operation": "multiply"}}
   │
   ▼
execute_tool_call(spec)   →  294
```

## Try these once it runs

1. Ask "What is 42 * 7?" — model should request calculator with multiply
2. Ask "What's the capital of France?" — model should NOT request any tool (and `request_tool` returns `None`)
3. Ask "Add 100 and 200" — model should request calculator with add
4. Manually call `execute_tool_call({"tool": "calculator", "arguments": {"a": 10, "b": 5, "operation": "divide"}})` — pure dispatch, no LLM

## Output
```bash
Q: What is 42 times 7?
  → requested: {'tool': 'calculator', 'arguments': {'a': 42, 'b': 7, 'operation': 'multiply'}}
  → result:    294

Q: Add 100 and 200.
  → requested: {'tool': 'calculator', 'arguments': {'a': 100, 'b': 200, 'operation': 'add'}}
  → result:    300

Q: Subtract 50 from 1000.
  → requested: {'tool': 'calculator', 'arguments': {'a': 1000, 'b': 50, 'operation': 'subtract'}}
  → result:    950

Q: Divide 144 by 12.
  → requested: {'tool': 'calculator', 'arguments': {'a': 144, 'b': 12, 'operation': 'divide'}}
  → result:    12.0

Q: What's the capital of France?
  → requested: {'tool': 'wikipedia', 'arguments': {'query': 'capital of France'}}
  → tool error: Unknown tool: wikipedia
```
