from arc_agent.utils import print_grid

def is_horizontally_symmetric(grid):
    return all(row == row[::-1] for row in grid)

def vertical_mirror(grid):
    return grid[::-1]

def solve_task_logic(task):
    """
    Rule 1: If input is all 0s → fill with 1s
    Rule 2: If input contains one unique non-zero value → fill grid with that value
    Rule 3: If grid is horizontally symmetric → return vertically mirrored grid
    """
    test_outputs = []

    for test in task["test"]:
        grid = test["input"]
        flat = [cell for row in grid for cell in row]

        # Rule 1: all 0s → fill with 1s
        if all(cell == 0 for cell in flat):
            output = [[1 for _ in row] for row in grid]

        # Rule 3: if grid is horizontally symmetric → return vertically mirrored
        elif is_horizontally_symmetric(grid):
            output = vertical_mirror(grid)

        # Rule 2: only one unique non-zero value → fill with that
        elif len(set(flat)) == 2 and 0 in flat:
            non_zero_vals = [v for v in flat if v != 0]
            if len(set(non_zero_vals)) == 1:
                val = non_zero_vals[0]
                output = [[val for _ in row] for row in grid]
            else:
                output = grid

        else:
            output = grid  # fallback

        test_outputs.append(output)

    return test_outputs