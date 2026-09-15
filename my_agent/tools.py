"""
Tools — APIs the agent can request, but never executes directly.

Tools are NOT abilities the model has. They're functions you wrote
that the model can name + parameterize via JSON. You keep control
of what actually runs.

Lesson 05 adds the first tool: a calculator. Each lesson after this
can add more (a search, a database lookup, a file reader, etc.).
"""

# The actual implementations. The agent never calls these directly;
# execute_tool() does, after validating the model's request.
def calculator(a, b, operation="add"):
    operations = {
        "add":      lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide":   lambda x, y: x / y if y != 0 else float("inf"),
    }
    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")
    return operations[operation](a, b)


# Registry — name -> function
TOOLS = {
    "calculator": calculator,
}


def get_tool_schema():
    """
    Returns the schema the agent sees in the prompt.

    This is the "menu" you show the model. It tells the model what
    tools exist, what they do, and what parameters they take.
    """
    return {
        "calculator": {
            "description": "Perform basic arithmetic operations",
            "parameters": {
                "a":         {"type": "number", "description": "First number"},
                "b":         {"type": "number", "description": "Second number"},
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "Which operation to perform",
                },
            },
            "required": ["a", "b"],
        }
    }


def execute_tool(tool_name, arguments):
    """
    Run a tool by name with the given arguments.

    This is the only place tools actually execute. The agent
    hands you a JSON spec; you dispatch.
    """
    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")
    return TOOLS[tool_name](**arguments)
