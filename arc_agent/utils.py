from arc_agent.debug_tools import print_grid

def learn_patterns_from_training(grid):
    """
    Detects all repeating symbolic patterns from the training input.
    Returns a list of (start_x, pattern, leading_symbol) tuples.
    """
    patterns = []
    for y, row in enumerate(grid):
        symbols = [(x, val) for x, val in enumerate(row) if val != 0]
        if len(symbols) >= 2:
            # sort by x-position
            symbols.sort()
            pattern = []
            last_x = symbols[0][0]
            pattern.append(symbols[0][1])
            for i in range(1, len(symbols)):
                gap = symbols[i][0] - last_x - 1
                pattern.extend([0] * gap)
                pattern.append(symbols[i][1])
                last_x = symbols[i][0]
            start_x = symbols[0][0]
            leading = symbols[0][1]
            patterns.append((start_x, pattern, leading))
    return patterns

def apply_patterns_to_test_grid(grid, learned_patterns):
    """
    For each test row, apply all matching patterns from training sequentially if any symbol matches.
    Returns the new grid and a log of applied patterns.
    """
    height = len(grid)
    width = len(grid[0])
    output = [row.copy() for row in grid]
    application_logs = []

    for y in range(height):
        row = grid[y]
        result_row = list(row)
        log_row = []

        for pattern_idx, (start_x, pattern, lead) in enumerate(learned_patterns):
            match_found = False
            for i in range(len(result_row) - len(pattern) + 1):
                if result_row[i] == lead:
                    segment = result_row[i:i + len(pattern)]
                    if all((s == p or p == 0) for s, p in zip(segment, pattern)):
                        result_row[i:i + len(pattern)] = pattern
                        match_found = True
                        log_row.append({
                            "pattern_idx": pattern_idx,
                            "start_x": start_x,
                            "applied_at": i,
                            "pattern": pattern
                        })
            if not match_found:
                log_row.append({"pattern_idx": pattern_idx, "applied_at": None})

        output[y] = result_row
        application_logs.append(log_row)

    return output
