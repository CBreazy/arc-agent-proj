from arc_agent.utils import print_grid

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
    For each test row, apply a matching pattern from training if a known symbol is found.
    """
    height = len(grid)
    width = len(grid[0])
    output = [row.copy() for row in grid]

    for y in range(height):
        row = grid[y]
        row_syms = [val for val in row if val != 0]
        if not row_syms:
            continue

        matched = False
        for (start_x, pattern, leading) in learned_patterns:
            if any(symbol in row_syms for symbol in pattern):
                # Apply this pattern
                new_row = [0] * width
                for x in range(start_x, width, len(pattern)):
                    for i, val in enumerate(pattern):
                        if x + i < width:
                            new_row[x + i] = val
                output[y] = new_row
                matched = True
                break

        if not matched:
            # Default to original row if no pattern matched
            output[y] = row.copy()

    return output


# ==========================
# RULE DEFINITIONS
# ==========================

def rule_all_zeros(grid):
    """If all cells are 0 → fill grid with 1s"""
    flat = [cell for row in grid for cell in row]
    if all(cell == 0 for cell in flat):
        output = [[1 for _ in row] for row in grid]
        return True, output
    return False, None

def rule_horizontal_symmetry(grid):
    """If grid is horizontally symmetric → return vertical mirror"""
    if all(row == row[::-1] for row in grid):
        return True, grid[::-1]
    return False, None

def rule_fill_with_constant(grid):
    """If only one non-zero value exists → fill grid with that value"""
    flat = [cell for row in grid for cell in row]
    if len(set(flat)) == 2 and 0 in flat:
        non_zero_vals = [v for v in flat if v != 0]
        if len(set(non_zero_vals)) == 1:
            val = non_zero_vals[0]
            output = [[val for _ in row] for row in grid]
            return True, output
    return False, None

def rule_fill_diagonal(grid):
    if len(grid) == len(grid[0]):  # must be square
        n = len(grid)
        output = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        return True, output
    return False, None

def rule_repeat_observed_pattern(grid):
    """
    For each row, detect a minimal repeating pattern using non-zero values.
    If a valid pattern is found on one row, reuse it on all other rows.
    """
    height = len(grid)
    width = len(grid[0])
    output = [row.copy() for row in grid]
    rule_applied = False
    fallback_pattern = None
    fallback_start = 0

    for y in range(height):
        row = grid[y]
        symbols = [(x, row[x]) for x in range(len(row)) if row[x] != 0]

        if fallback_pattern is None and len(symbols) >= 2 and len(set(val for _, val in symbols)) >= 2:
            # Build pattern for this row
            symbols.sort(key=lambda tup: tup[0])
            pattern = []
            last_x = symbols[0][0]
            pattern.append(symbols[0][1])
            for i in range(1, len(symbols)):
                gap = symbols[i][0] - last_x - 1
                pattern.extend([0] * gap)
                pattern.append(symbols[i][1])
                last_x = symbols[i][0]
            fallback_pattern = pattern
            fallback_start = symbols[0][0]

            print(f"📦 Learned fallback pattern: {fallback_pattern} starting at x={fallback_start}")

        if fallback_pattern and y != 0:
            print(f"🔁 Applying fallback pattern to row {y}")
            # Apply the most recent pattern to this row
            new_row = [0] * width
            for x in range(fallback_start, width, len(fallback_pattern)):
                for i, val in enumerate(fallback_pattern):
                    if x + i < width:
                        new_row[x + i] = val
            output[y] = new_row
            rule_applied = True

    return (True, output) if rule_applied else (False, None)


def extract_nonzero_positions(grid):
    """Extract all non-zero positions"""
    positions = []
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val != 0:
                positions.append((x, y, val))
    return positions

def infer_horizontal_repeat(grid):
    """
    If two non-zero values exist on the same row with consistent spacing, return the delta.
    """
    symbols = extract_nonzero_positions(grid)
    horizontal_deltas = []

    for i in range(len(symbols)):
        for j in range(i + 1, len(symbols)):
            x1, y1, val1 = symbols[i]
            x2, y2, val2 = symbols[j]

            # Only compare same-row elements with different values
            if y1 == y2 and val1 != val2:
                dx = abs(x2 - x1)
                if dx > 0:
                    horizontal_deltas.append(dx)

    # Return most common delta if any were found
    if horizontal_deltas:
        from collections import Counter
        most_common = Counter(horizontal_deltas).most_common(1)[0][0]
        return most_common

    return None

def propagate_symbols_horizontally(grid, delta, sym1, sym2):
    """
    Use the actual pattern between sym1 and sym2 to replicate it horizontally.
    """
    height = len(grid)
    width = len(grid[0])
    output = [row.copy() for row in grid]

    for y in range(height):
        row = grid[y]
        row_symbols = [(x, row[x]) for x in range(len(row)) if row[x] != 0]

        if len(row_symbols) < 2:
            continue

        row_symbols.sort()  # sort by x
        pattern = []
        last_x = row_symbols[0][0]
        pattern.append(row_symbols[0][1])

        for i in range(1, len(row_symbols)):
            gap = row_symbols[i][0] - last_x - 1
            pattern.extend([0] * gap)
            pattern.append(row_symbols[i][1])
            last_x = row_symbols[i][0]

        pattern_len = len(pattern)
        for x in range(row_symbols[0][0], width, pattern_len):
            for i, val in enumerate(pattern):
                if x + i < width:
                    output[y][x + i] = val

    return output



# ==========================
# MAIN SOLVER LOGIC
# ==========================

def solve_task_logic(task):
    rules = [
        rule_all_zeros, 
        rule_horizontal_symmetry, 
        rule_fill_with_constant, 
        rule_fill_diagonal, 
        # rule_repeat_observed_pattern
    ]

    train_grid = task["train"][0]["input"]
    learned_patterns = learn_patterns_from_training(train_grid)

    test_outputs = []
    for test in task["test"]:
        test_output = apply_patterns_to_test_grid(test["input"], learned_patterns)
        test_outputs.append(test_output)

    return test_outputs