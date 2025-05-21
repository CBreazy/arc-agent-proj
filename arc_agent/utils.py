def print_grid(grid):
    for row in grid:
        print(' '.join(str(cell) for cell in row))
    print("\n")

def compare_grids(grid1, grid2):
    if len(grid1) != len(grid2) or len(grid1[0]) != len(grid2[0]):
        return 0.0  # size mismatch

    total = 0
    match = 0
    for row1, row2 in zip(grid1, grid2):
        for c1, c2 in zip(row1, row2):
            total += 1
            if c1 == c2:
                match += 1

    return match / total if total > 0 else 0.0

def compare_grids_with_tolerance(grid1, grid2, tolerance=0.1):
    """
    Compare two grids with a tolerance level.
    """
    if len(grid1) != len(grid2) or len(grid1[0]) != len(grid2[0]):
        return 0.0  # size mismatch

    total = 0
    match = 0
    for row1, row2 in zip(grid1, grid2):
        for c1, c2 in zip(row1, row2):
            total += 1
            if abs(c1 - c2) <= tolerance:
                match += 1

    return match / total if total > 0 else 0.0