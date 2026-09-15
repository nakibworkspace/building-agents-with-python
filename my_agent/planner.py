"""
Planning — data generation, not reasoning.

Plans are inspectable, modifiable Python data structures.
This file holds the three planning functions used in L08–L10.
"""


def create_plan(llm, goal):
    """
    Ask the model to produce an ordered list of steps to reach `goal`.

    Returns a dict like {"steps": ["step1", "step2", ...]} or None.
    """
    from my_agent.utils import extract_json_from_text

    prompt = f"""Create a step-by-step plan to achieve the goal. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{"steps": ["step1", "step2", "step3"]}}

Goal: {goal}

Response (JSON only):"""

    for attempt in range(3):
        response = llm.generate(prompt, temperature=0.0)
        plan = extract_json_from_text(response)
        if plan and "steps" in plan and isinstance(plan["steps"], list):
            return plan

    return None


def create_atomic_action(llm, step):
    """
    Decompose a single plan step into an atomic action with explicit inputs.

    An atomic action is the smallest possible unit:
      - one action name (verb-like)
      - one inputs dict (its parameters)

    Returns dict like {"action": "write_definition", "inputs": {"topic": "HTTPS"}}
    or None on failure.
    """
    from my_agent.utils import extract_json_from_text

    prompt = f"""Convert this step into an atomic action. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{
  "action": "action_name",
  "inputs": {{"key": "value"}}
}}

The action should be a simple, atomic operation name.
The inputs should be a dictionary with the parameters needed for this action.

Step to convert:
{step}

Response (JSON only):"""

    for attempt in range(3):
        response = llm.generate(prompt, temperature=0.0)
        action = extract_json_from_text(response)
        if action and "action" in action:
            return action

    return None


def create_aot_graph(llm, goal):
    """
    Generate an Atom of Thought (AoT) execution graph for the goal.

    Each node is an atomic action. `depends_on` lists node IDs that
    must complete first.

    Returns dict like:
      {"nodes": [
          {"id": "1", "action": "research", "depends_on": []},
          {"id": "2", "action": "write",    "depends_on": ["1"]},
      ]}
    or None on failure.
    """
    from my_agent.utils import extract_json_from_text

    prompt = f"""Create an atomic execution graph for the goal. Each node is a single action. Dependencies are node IDs. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{"nodes": [{{"id": "1", "action": "research", "depends_on": []}}, {{"id": "2", "action": "write", "depends_on": ["1"]}}]}}

Each node must have:
- id: unique string like "1", "2", "3"
- action: what to do (e.g., "research", "write", "review")
- depends_on: list of node IDs that must complete first (empty [] for first step)

Goal: {goal}

Response (JSON only):"""

    for attempt in range(3):
        response = llm.generate(prompt, temperature=0.0)
        graph = extract_json_from_text(response)
        if graph and "nodes" in graph and isinstance(graph["nodes"], list):
            # Validate every node has id + action + depends_on
            valid = []
            for node in graph["nodes"]:
                if (
                    isinstance(node, dict)
                    and "id" in node
                    and "action" in node
                    and "depends_on" in node
                    and isinstance(node["depends_on"], list)
                ):
                    valid.append(node)
            if valid:
                return {"nodes": valid}

    return None


def execute_graph(graph, executor_func):
    """
    Execute an AoT graph respecting dependencies (simple topological execution).

    Iterates until all nodes are done (or max iterations reached as safety).
    Each call to executor_func(action_str) returns a result string.
    """
    if not graph or "nodes" not in graph:
        return []

    nodes = graph["nodes"]
    executed = set()
    results = []
    max_iterations = len(nodes) * 2

    iteration = 0
    while len(executed) < len(nodes) and iteration < max_iterations:
        iteration += 1
        for node in nodes:
            node_id = node["id"]
            if node_id in executed:
                continue

            deps = node.get("depends_on", [])
            if all(d in executed for d in deps):
                try:
                    result = executor_func(node["action"])
                    results.append({
                        "node_id": node_id,
                        "action": node["action"],
                        "result": result,
                        "success": True,
                    })
                except Exception as e:
                    results.append({
                        "node_id": node_id,
                        "action": node["action"],
                        "error": str(e),
                        "success": False,
                    })
                executed.add(node_id)  # mark even on failure to avoid loops

    return results
