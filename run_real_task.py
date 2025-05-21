import json
import sys
import os

# Adjust path for local imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "arc_agent")))

from arc_agent.solve import solve
from arc_agent.utils import print_grid


def load_task(path):
    with open(path, 'r') as f:
        return json.load(f)

def run_task(task_path):
    task = load_task(task_path)
    print(f"🔍 Running ARC Task: {os.path.basename(task_path)}\n")

    for i, pair in enumerate(task['train']):
        print(f"🧪 Train Pair {i + 1} — Input:")
        print_grid(pair['input'])
        print("Expected Output:")
        print_grid(pair['output'])

    predictions = solve(task)

    for i, output in enumerate(predictions):
        print(f"🔮 Test Output {i + 1}:")
        print_grid(output)

if __name__ == "__main__":
    # Example usage: python run_real_task.py data/ARC/data/training/6b9890af.json
    if len(sys.argv) < 2:
        print("Usage: python run_real_task.py <task_file.json>")
    else:
        run_task(sys.argv[1])
