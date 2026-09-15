"""
Memory — explicit storage. NOT consciousness.

A list of strings the agent can refer to across turns.
Plain Python. No magic. No embeddings yet. Just a list.
"""


class Memory:
    def __init__(self):
        self.items = []

    def add(self, item):
        if item and item not in self.items:
            self.items.append(item)

    def get_all(self):
        return self.items.copy()

    def search(self, query):
        q = query.lower()
        return [item for item in self.items if q in item.lower()]

    def clear(self):
        self.items = []

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f"Memory({len(self.items)} items)"
