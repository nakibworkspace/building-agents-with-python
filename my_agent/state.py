"""
AgentState — explicit, inspectable state.

State is NOT hidden in conversation history or mysterious context.
It's just a Python object you can read, modify, and reason about.
"""

class AgentState:
    """
    The agent's working memory for one task.

    Grows lesson by lesson:
      L06: basic (steps, done)
      L08: adds planning state
    """

    def __init__(self):
        self.steps = 0
        self.done = False

    def increment_step(self):
        self.steps += 1

    def mark_done(self):
        self.done = True

    def reset(self):
        self.steps = 0
        self.done = False

    def to_dict(self):
        return {"steps": self.steps, "done": self.done}
