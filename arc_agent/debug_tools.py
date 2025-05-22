# arc_agent/debug_tools.py
def print_grid(grid):
    for row in grid:
        print(''.join(str(cell) for cell in row))
    print()
