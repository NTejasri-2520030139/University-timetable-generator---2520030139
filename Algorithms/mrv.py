"""
algorithms/mrv.py — Minimum Remaining Values Heuristic
CO3: Variable ordering for backtracking search.

MRV selects the unassigned variable whose domain has the fewest
remaining legal values — the "most constrained" variable.
This reduces the branching factor and detects failures early.
"""


def mrv(variables, domains, assignment):
    """
    MRV (Minimum Remaining Values) Heuristic.

    From all unassigned variables, selects the one with the
    smallest remaining domain size. Ties broken by Degree heuristic.

    Args:
        variables  : list of all CSP variables
        domains    : dict variable -> list of remaining values
        assignment : dict of current assignments

    Returns:
        The variable with minimum remaining values.
    """
    unassigned = [v for v in variables if v not in assignment]
    if not unassigned:
        return None

    # Find minimum domain size
    min_size = min(len(domains[v]) for v in unassigned)

    # Collect all variables tied at minimum
    mrv_vars = [v for v in unassigned if len(domains[v]) == min_size]

    return mrv_vars  # Return list; degree.py breaks ties
