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
        # TODO(L05): build a prompt that:
        #   1) Shows the tool schema (use get_tool_schema())
        #   2) Tells the model to respond with JSON:
        #      {"tool": "<name>", "arguments": {<params>}}
        #   3) Asks the question (use {user_input})
        #
        # Then loop up to 3 times:
        #   - self.llm.generate(prompt, temperature=0.0)
        #   - extract_json_from_text(response)
        #   - if parsed has "tool" and "arguments" keys, return parsed
        #
        # Return None on failure.
        raise NotImplementedError("Implement Lesson 05: request_tool")

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

