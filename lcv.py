"""
algorithms/degree.py — Degree Heuristic
CO3: Tie-breaking for MRV variable selection.

The Degree Heuristic selects the variable involved in the
greatest number of constraints with *other unassigned* variables.
It is used to break ties when multiple variables share the same MRV score.
"""


def degree_heuristic(candidates, neighbors, assignment):
    """
    Degree Heuristic — break MRV ties by constraint degree.

    Among candidate variables (already filtered by MRV), selects
    the one with the most constraints on remaining unassigned variables.

    Args:
        candidates : list of variable names (MRV-tied)
        neighbors  : dict variable -> set of neighboring variables
        assignment : dict of current assignments

    Returns:
        Single variable with highest degree among candidates.
    """
    unassigned_set = set(v for v in neighbors if v not in assignment)

    best_var = None
    best_degree = -1

    for var in candidates:
        # Count constraints with unassigned neighbors only
        degree = len(neighbors.get(var, set()) & unassigned_set)
        if degree > best_degree:
            best_degree = degree
            best_var = var

    return best_var if best_var is not None else candidates[0]


def select_variable(variables, domains, neighbors, assignment):
    """
    Combined MRV + Degree variable selection.

    1. Use MRV to get candidates with fewest remaining values.
    2. Use Degree to break ties among MRV candidates.

    Returns:
        The best variable to assign next.
    """
    from algorithms.mrv import mrv
    candidates = mrv(variables, domains, assignment)
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    return degree_heuristic(candidates, neighbors, assignment)
