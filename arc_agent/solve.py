def solve(task):
    """
    Main ARC interface. Receives a task dict and returns a list of predicted output grids.
    """
    from .engine import solve_task_logic
    return solve_task_logic(task)
