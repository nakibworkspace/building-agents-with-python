"""
Boring plumbing: turn messy LLM text into clean data.

The LLM doesn't reliably return pure JSON. Sometimes it:
  - wraps in ```json fences
  - adds prose like "Here's the JSON: {...}"
  - forgets to close a string
  - rambles before getting to the object

extract_json_from_text tries a ladder of progressively more forgiving
strategies until one returns a valid dict, or returns None.
"""

import json


def safe_json_parse(text):
    """json.loads wrapped in try/except. Returns None on failure."""
    if not text:
        return None
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None


def extract_json_from_text(text):
    """
    Pull a JSON object out of text that may contain extra noise.
    Returns a dict, or None if nothing parseable is found.
    """
    if not text:
        return None

    # Strip markdown code fences
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    # Strip prose prefixes
    for prefix in ["JSON:", "Response:", "Answer:", "Here's the JSON:", "The JSON is:"]:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()

    # Try direct parse
    result = safe_json_parse(text)
    if result is not None:
        return result

    # Find first {...} or [...]
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        snippet = text[start:end + 1]
        result = safe_json_parse(snippet)
        if result is not None:
            return result

    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        snippet = text[start:end + 1]
        result = safe_json_parse(snippet)
        if result is not None:
            return result

    return None
