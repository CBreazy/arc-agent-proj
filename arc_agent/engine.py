from arc_agent.utils import print_grid

def learn_patterns_from_training(grid):
    """
    Extracts simple symbol-based patterns from the grid.
    Returns a list of (start_x, pattern, leading_symbol, roles) tuples.
    """
    patterns = []
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val != 0:
                pattern = [val]
                roles = ['starter']
                print(f"📚 Learned single-symbol pattern at x={x}: [{val}] with roles {roles}")
                patterns.append((x, pattern, val, roles))
    print(f"✅ Total patterns learned: {len(patterns)}")
    return patterns

def segment_grid_into_bands(grid, band_height):
    """
    Splits the grid into horizontal bands of equal height.
    """
    return [grid[i:i + band_height] for i in range(0, len(grid), band_height)]

def apply_patterns_to_test_grid(grid, learned_patterns):
    import sys
    """
    For each test row, re-apply all matching patterns from training until convergence.
    Returns the new grid and a log of applied patterns.
    """
    height = len(grid)
    width = len(grid[0])
    output = [row.copy() for row in grid]
    application_logs = []

    for y in range(height):
        result_row = list(grid[y])
        log_row = []
        changes_made = True

        while changes_made:
            changes_made = False
            for pattern_idx, (start_x, pattern, lead, roles) in enumerate(learned_patterns):
                try:
                    starter_offset = roles.index('starter')
                    starter_val = pattern[starter_offset]
                except ValueError:
                    continue  # no starter role found
                for apply_at in range(len(result_row) - len(pattern) + 1):
                    check_pos = apply_at + starter_offset
                    if check_pos >= len(result_row):
                        continue
                    if result_row[check_pos] != starter_val:
                        continue
                    segment = result_row[apply_at:apply_at + len(pattern)]
                    if all((s == p or p == 0) for s, p in zip(segment, pattern)):
                            if len(pattern) == 1:
                                fill_val = pattern[0]
                                for i in range(apply_at, len(result_row)):
                                    result_row[i] = fill_val
                            else:
                                result_row[apply_at:apply_at + len(pattern)] = pattern
                                changes_made = True
                                log_row.append({
                                    "pattern_idx": pattern_idx,
                                    "start_x": start_x,
                                    "applied_at": apply_at,
                                    "pattern": pattern,
                                    "roles": roles
                                })
        output[y] = result_row
        application_logs.append(log_row)

    # Print application logs for diagnostics
    for row_idx, log_row in enumerate(application_logs):
        if log_row:
            pattern_ids = [entry['pattern_idx'] for entry in log_row]
            print(f"🧩 Row {row_idx}: Patterns applied {pattern_ids}", file=sys.stderr)
        else:
            print(f"⚠️ Row {row_idx}: No patterns applied", file=sys.stderr)

    return output

def solve_task_logic(task):
    rules = []

    all_patterns = []
    for pair in task["train"]:
        train_grid = pair["input"]
        patterns = learn_patterns_from_training(train_grid)
        all_patterns.extend(patterns)
    learned_patterns = all_patterns

    test_outputs = []
    for test in task["test"]:
        test_input = test["input"]
        banded_input = segment_grid_into_bands(test_input, band_height=1)  # band_height can be adjusted
        flattened_output = []
        for band in banded_input:
            band_output = apply_patterns_to_test_grid(band, learned_patterns)
            flattened_output.extend(band_output)
        test_outputs.append(flattened_output)

    return test_outputs
