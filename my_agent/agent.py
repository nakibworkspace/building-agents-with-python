"""
Agent — built lesson by lesson.

Lesson 01: just text in, text out.
Later lessons will add: roles, structured output, decisions, tools, loops, memory, planning, AoT.

You implement each lesson's method yourself. Don't peek at the reference repo
until you've tried.
"""

from llm import LocalLLM
from my_agent.utils import extract_json_from_text
from my_agent.tools import get_tool_schema, execute_tool
from my_agent.state import AgentState
from my_agent.memory import Memory
from my_agent.planner import create_plan, create_atomic_action


class Agent:
    """
    My agent. Grows one capability per lesson.
    """

    def __init__(self, model_path: str):
        # The LocalLLM seam is provider-agnostic.
        # For Ollama: pass "ollama:llama3.2:latest"
        self.llm = LocalLLM(model_path)

        # Lesson 02: a default persona lives on the agent.
        # Replace this with any persona you want — it's just a string
        # prepended to the prompt. No magic.
        self.system_prompt = (
            "You are a calm, precise, and helpful AI assistant. "
            "You explain concepts simply and avoid unnecessary jargon. "
            "You are honest about what you know and don't know."
        )

        # Lesson 06: explicit, inspectable state.
        self.state = AgentState()

        # Lesson 07: memory persists across turns.
        self.memory = Memory()

    # ============================================================
    # LESSON 01 — implement me!
    # ============================================================

    def simple_generate(self, user_input: str) -> str:
        """
        Send `user_input` to the model and return the raw text response.

        That's it. One line should do it.

        Args:
            user_input: the user's prompt (a string)
        Returns:
            the model's response (a string)
        """
        return self.llm.generate(user_input)

    # ============================================================
    # LESSON 02 — implement me!
    # ============================================================

    def generate_with_role(self, user_input: str) -> str:
        """
        Generate with a system prompt to shape behavior.

        Lesson 02 version.

        Args:
            user_input: the user's prompt

        Returns:
            the model's response with role-based behavior
        """
        prompt = f"{self.system_prompt}\n\nUser: {user_input}\nAssistant:"
        response = self.llm.generate(prompt)
        response = response.replace('<SYSTEM>', '').replace('</SYSTEM>', '')
        response = response.replace('<USER>', '').replace('</USER>', '')
        return response.strip()

    # ============================================================
    # LESSON 03 — implement me!
    # ============================================================

    def generate_structured(self, user_input, schema):
        """
        Generate structured JSON output with validation and retries.

        Lesson 03 version.

        Args:
            user_input: the user's prompt
            schema:     a string describing the JSON shape you want back

        Returns:
            a parsed dict, or None if all retries failed
        """
        prompt = f"""{self.system_prompt}

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no extra text before or after the JSON
3. Start your response with {{ and end with }}

Schema you must follow:
{schema}

User request: {user_input}

Response (JSON only):"""

        for attempt in range(3):
            response = self.llm.generate(prompt, temperature=0.0)
            parsed = extract_json_from_text(response)

            if parsed is not None:
                return parsed

        return None

    # ============================================================
    # LESSON 04 — implement me!
    # ============================================================

    def decide(self, user_input, choices):
        """
        Make the model choose from a finite set of options.

        Lesson 04 version.

        Args:
            user_input: the input to make a decision about
            choices:    list of strings — the only valid answers

        Returns:
            one of the strings from choices, or None if all retries failed
        """
        options = "\n".join(f"- {choice}" for choice in choices)
        
        prompt = f"""{self.system_prompt}

You must choose ONE of the following options. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Available choices:
{options}

Required JSON format:
{{"decision": "one_of_the_choices_above"}}

User request: {user_input}

Response (JSON only):"""
        
        for attempt in range(3):
            response = self.llm.generate(prompt, temperature=0.0)
            parsed = extract_json_from_text(response)

            if parsed and "decision" in parsed:
                decision = parsed["decision"]
                if decision in choices:
                    return decision

        return None

    # ============================================================
    # LESSON 05 — implement me!
    # ============================================================

    def request_tool(self, user_input):
        """
        Ask the model to specify a tool call as JSON.

        Lesson 05 version.

        Args:
            user_input: the user's request

        Returns:
            dict like {"tool": "calculator", "arguments": {...}}, or None
        """
        prompt = f"""{self.system_prompt}

You are a tool-calling assistant. When asked a math question, you must respond with ONLY valid JSON.

Available tool: calculator
- Parameters: a (number), b (number), operation ("add", "subtract", "multiply", or "divide")

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Example format:
{{"tool": "calculator", "arguments": {{"a": 42, "b": 7, "operation": "multiply"}}}}

User request: {user_input}

Response (JSON only):"""
        
        for attempt in range(3):
            response = self.llm.generate(prompt, temperature=0.0)
            parsed = extract_json_from_text(response)

            if parsed and "tool" in parsed and "arguments" in parsed:
                return parsed
        
        return None


    def execute_tool_call(self, tool_call):
        """
        Run a tool the model requested.

        Args:
            tool_call: dict with "tool" (str) and "arguments" (dict)

        Returns:
            the tool's return value
        """
        # This one I'll write for you — it's pure dispatch.
        return execute_tool(tool_call["tool"], tool_call["arguments"])

    # ============================================================
    # LESSON 06 — implement me!
    # ============================================================

    def agent_step(self, user_input):
        """
        Execute ONE step of the agent loop: observe → decide → act.

        Lesson 06 version.

        Args:
            user_input: the user's request (the "observation")

        Returns:
            a dict like {"action": "analyze", "reason": "..."}, or None
        """
        state_dict = self.state.to_dict()

        prompt = f"""{self.system_prompt}

You are an agent. You must decide the next action and respond with ONLY valid JSON.

Current state: steps={state_dict.get('steps', 0)}, done={state_dict.get('done', False)}

Available actions: analyze, research, summarize, answer, done

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{"action": "action_name", "reason": "explanation"}}

User input: {user_input}

Response (JSON only):"""

        for attempt in range(3):
            response = self.llm.generate(prompt, temperature=0.0)
            parsed = extract_json_from_text(response)

            if parsed and "action" in parsed:
                if "reason" not in parsed:
                    parsed["reason"] = f"Taking action: {parsed['action']}"
                self.state.increment_step()
                return parsed

        return None


    def run_loop(self, user_input, max_steps=5):
        """
        Run the agent loop until done or max_steps reached.

        Args:
            user_input:  initial input
            max_steps:   safety limit

        Returns:
            list of action dicts from each step
        """
        self.state.reset()
        results = []

        while not self.state.done and self.state.steps < max_steps:
            action = self.agent_step(user_input)
            if action is None:
                break
            results.append(action)
            if action.get("action") == "done":
                self.state.mark_done()

        return results

    # ============================================================
    # LESSON 07 — implement me!
    # ============================================================

    def run_with_memory(self, user_input):
        """
        Run a single turn WITH memory context.

        Lesson 07 version.

        Args:
            user_input: the user's message

        Returns:
            dict like {"reply": "...", "save_to_memory": "..." or None}, or None
        """
        memory_context = self.memory.get_all()

        if memory_context:
            memory_str = "You remember the following:\n" + "\n".join(f"- {item}" for item in memory_context)
        else:
            memory_str = "You have no memories yet"
        
        prompt = f"""{self.system_prompt}

You are an agent with memory. You must respond with ONLY valid JSON.

{memory_str}

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}
4. If the user tells you information (like their name), save it to memory
5. If the user asks about something you remember, USE YOUR MEMORY to answer

Required JSON format:
{{"reply": "your response text", "save_to_memory": "fact to remember" or null}}

Examples:
- User says "My name is Alice" → {{"reply": "Nice to meet you, Alice!", "save_to_memory": "User's name is Alice"}}
- User asks "What's my name?" and you remember "User's name is Alice" → {{"reply": "Your name is Alice", "save_to_memory": null}}

User input: {user_input}

Response (JSON only):"""

        for attempt in range(3):
            response = self.llm.generate(prompt, temperature=0.0)
            parsed = extract_json_from_text(response)

            if parsed and "reply" in parsed:
                if parsed.get("save_to_memory"):
                    self.memory.add(parsed["save_to_memory"])

                self.state.increment_step()
                return parsed

        return None

    # ============================================================
    # LESSON 08 — implement me!
    # ============================================================

    def create_plan(self, goal):
        """
        Generate a plan to achieve a goal.

        Lesson 08 wrapper.

        Args:
            goal: the goal to achieve

        Returns:
            plan dict {"steps": [...]} or None
        """
        plan = create_plan(self.llm, goal)

        if plan:
            self.state.current_plan = plan

        return plan

    def execute_plan(self, plan):
        """
        Execute each step of a plan.

        Lesson 08 version — naive sequential execution, no real action.

        Args:
            plan: a dict with "steps" key (list of strings)

        Returns:
            list of result dicts
        """
        # I'll write this one for you — it's straightforward bookkeeping.
        if not plan or "steps" not in plan:
            return []

        results = []
        for step in plan["steps"]:
            # In a real agent, each step would call a tool. Here we just record.
            self.state.increment_step()
            results.append({"step": step, "executed": True})

        return results

    # ============================================================
    # LESSON 09 — implement me!
    # ============================================================

    def create_atomic_action(self, step):
        """
        Convert a single plan step into an atomic action.

        Lesson 09 wrapper.

        Args:
            step: a string — one step from a plan

        Returns:
            dict like {"action": "...", "inputs": {...}} or None
        """
        return create_atomic_action(self.llm, step)

