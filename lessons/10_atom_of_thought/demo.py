"""
Lesson 10 — Atom of Thought (AoT) demo.

Run from the agent-builder/ directory:
    python -m lessons.10_atom_of_thought.demo
"""

from my_agent import Agent


def main():
    agent = Agent("ollama:llama3.2:latest")

    goals = [
        "Write a short blog post comparing Python and JavaScript",
        "Plan a healthy weekly meal prep",
    ]

    for goal in goals:
        print(f"=== Goal: {goal} ===")
        graph = agent.create_aot_plan(goal)
        if graph is None:
            print("  (no graph generated)\n")
            continue

        print("Graph nodes:")
        for node in graph.get("nodes", []):
            print(f"  [{node['id']}] {node['action']}  depends_on={node['depends_on']}")
        print()

        results = agent.execute_aot_plan(graph)
        print(f"Executed {len(results)} nodes:")
        for r in results:
            status = "✓" if r["success"] else "✗"
            print(f"  {status} [{r['node_id']}] {r['action']}  →  {r.get('result', r.get('error'))}")
        print()


if __name__ == "__main__":
    main()
