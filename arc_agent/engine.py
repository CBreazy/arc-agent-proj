def solve_task_logic(task):
    """
    Rule 1: If input is all 0s → output is all 1s
    Rule 2: If grid has only one non-zero number → fill grid with that number
    """
    test_outputs = []

    for test in task["test"]:
        grid = test["input"]
        flat = [cell for row in grid for cell in row]

        # Rule 1: all 0s → fill with 1s
        if all(cell == 0 for cell in flat):
            output = [[1 for _ in row] for row in grid]

        # Rule 2: only one unique non-zero value → fill with that
        else:
            non_zero = [v for v in flat if v != 0]
            if len(set(non_zero)) == 1:
                fill_val = non_zero[0]
                output = [[fill_val for _ in row] for row in grid]
            else:
                output = grid  # fallback

        test_outputs.append(output)

    return test_outputs
