import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Sample ARC test input (to be replaced with actual tasks)
sample_task = {
    "train": [{"input": [[0, 0, 0, 0, 0, 2, 0, 8, 0, 0]],
               "output": [[0, 0, 0, 0, 0, 2, 0, 8, 0, 0]]}],
    "test": [{"input": [[0, 0, 0, 0, 0, 2, 0, 8, 0, 0]]}]
}

if __name__ == "__main__":
    from arc_agent.solve import solve
    from arc_agent.utils import print_grid

    print("Running sample ARC task...")
    from arc_agent.engine import infer_horizontal_repeat

    test_grid = sample_task["test"][0]["input"]
    delta = infer_horizontal_repeat(test_grid)
    print(f"Inferred horizontal repeat delta: {delta}")

    predictions = solve(sample_task)
    for grid in predictions:
        print_grid(grid)
