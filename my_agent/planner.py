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
