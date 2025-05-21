from arc_agent.utils import print_grid

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
    Detects repeatable symbol patterns in a row and reproduces them across the row.
    Triggers only if two or more non-zero symbols appear in sequence.
    """
    symbols = extract_nonzero_positions(grid)
    delta = infer_horizontal_repeat(grid)

    if not delta or len(symbols) < 2:
        return False, None

    # Get the two most common distinct symbols from the same row
    same_row = [s for s in symbols if s[1] == symbols[0][1]]  # restrict to row of first symbol
    distinct_vals = list(set(s[2] for s in same_row))
    if len(distinct_vals) < 2:
        return False, None

    sym1, sym2 = distinct_vals[:2]
    output = propagate_symbols_horizontally(grid, delta, sym1, sym2)
    return True, output


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

    # Build the pattern based on input grid slice
    # Find their x-positions on the same row
    symbols = extract_nonzero_positions(grid)
    for y in range(height):
        row_symbols = [s for s in symbols if s[1] == y]
        if len(row_symbols) >= 2:
            row_symbols.sort()  # sort by x
            pattern = []
            last_x = row_symbols[0][0]
            pattern.append(row_symbols[0][2])
            for i in range(1, len(row_symbols)):
                gap = row_symbols[i][0] - last_x - 1
                pattern.extend([0] * gap)
                pattern.append(row_symbols[i][2])
                last_x = row_symbols[i][0]

            # Now repeat this pattern across the row
            pattern_len = len(pattern)
            for x in range(0, width, pattern_len):
                for i, val in enumerate(pattern):
                    if x + i < width:
                        output[y][x + i] = val

    return output




# ==========================
# MAIN SOLVER LOGIC
# ==========================

def solve_task_logic(task):
    rules = [rule_all_zeros, rule_horizontal_symmetry, rule_fill_with_constant, rule_fill_diagonal, rule_repeat_observed_pattern]
    test_outputs = []

    for test in task["test"]:
        grid = test["input"]
        matched = False
        for rule in rules:
            result, output = rule(grid)
            if result:
                matched = True
                break
        if not matched:
            output = grid  # fallback
        test_outputs.append(output)

    return test_outputs
