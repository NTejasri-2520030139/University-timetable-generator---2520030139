"""
algorithms/lcv.py — Least Constraining Value Heuristic
CO3: Value ordering for backtracking search.

LCV orders domain values by how few options they eliminate for
neighboring unassigned variables. Values that "rule out" the
fewest choices for neighbors are tried first, maximizing the
chance of finding a solution without backtracking.
"""


def lcv(var, domain_values, neighbors, domains, constraints, assignment):
    """
    LCV (Least Constraining Value) Heuristic.

    Sorts domain values of `var` by ascending conflict count —
    i.e., how many values are eliminated from neighbors' domains
    if this value is assigned to `var`.

    Args:
        var           : variable being assigned
        domain_values : current domain of var
        neighbors     : dict variable -> set of neighboring variables
        domains       : dict variable -> list of remaining values
        constraints   : dict variable -> list of (neighbor, fn) pairs
        assignment    : current assignment dict

    Returns:
        Sorted list of values (least constraining first).
    """
    unassigned_neighbors = [
        nb for nb in neighbors.get(var, set())
        if nb not in assignment
    ]

    if not unassigned_neighbors:
        return list(domain_values)

    def conflict_count(val):
        """Count how many neighbor values would be eliminated by assigning val."""
        total = 0
        for nb in unassigned_neighbors:
            fns = [fn for (n, fn) in constraints.get(var, []) if n == nb]
            for nb_val in domains[nb]:
                if not all(fn(val, nb_val) for fn in fns):
                    total += 1
        return total

    return sorted(domain_values, key=conflict_count)
