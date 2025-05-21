import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Sample ARC test input (to be replaced with actual tasks)
sample_task = {
    "train": [{"input": [[2, 0], [0, 0]], "output": [[2, 2], [2, 2]]}],
    "test": [{"input": [[0, 0], [2, 0]]}]
}

if __name__ == "__main__":
    from arc_agent.solve import solve
    from arc_agent.utils import print_grid

    print("Running sample ARC task...")
    predictions = solve(sample_task)
    for grid in predictions:
        print_grid(grid)
