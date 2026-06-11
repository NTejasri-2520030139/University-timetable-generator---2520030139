"""
algorithms/csp.py — Core CSP Framework
CO3: Models the timetable scheduling as a Constraint Satisfaction Problem.

Variables  : Each (subject) that needs a session scheduled
Domains    : All valid (teacher, classroom, timeslot) combinations
Constraints: Hard constraints preventing conflicts
"""

from collections import deque


class CSP:
    """
    Generic Constraint Satisfaction Problem framework.
    Used to model university timetable generation as a CSP.
    """

    def __init__(self):
        self.variables = []       # list of variable names
        self.domains = {}         # var -> list of possible values
        self.constraints = {}     # var -> list of constraint functions
        self.neighbors = {}       # var -> set of neighboring vars
        self.metrics = {
            'backtracks': 0,
            'constraint_checks': 0,
            'ac3_pruned': 0,
        }

    def add_variable(self, var, domain):
        """Register a variable with its initial domain."""
        self.variables.append(var)
        self.domains[var] = list(domain)
        self.constraints[var] = []
        self.neighbors[var] = set()

    def add_constraint(self, var1, var2, fn):
        """
        Add a binary constraint between var1 and var2.
        fn(val1, val2) -> bool: True if consistent.
        """
        self.constraints[var1].append((var2, fn))
        self.constraints[var2].append((var1, lambda b, a: fn(a, b)))
        self.neighbors[var1].add(var2)
        self.neighbors[var2].add(var1)

    def is_consistent(self, var, value, assignment):
        """Check if assigning value to var is consistent with current assignment."""
        for neighbor, fn in self.constraints[var]:
            if neighbor in assignment:
                self.metrics['constraint_checks'] += 1
                if not fn(value, assignment[neighbor]):
                    return False
        return True

    # ── AC-3: Arc Consistency Propagation ─────────────────────────────────
    def ac3(self, domains=None):
        """
        AC-3 Algorithm — enforces arc consistency to prune domains.

        For every arc (Xi, Xj), removes values from Xi's domain that
        have no support in Xj's domain. Re-queues arcs when domain shrinks.

        Returns False if any domain is wiped out (no solution possible).
        """
        if domains is None:
            domains = self.domains

        queue = deque()
        for var in self.variables:
            for neighbor, _ in self.constraints[var]:
                queue.append((var, neighbor))

        while queue:
            xi, xj = queue.popleft()
            if self._revise(domains, xi, xj):
                if len(domains[xi]) == 0:
                    return False   # Domain wipe-out
                # Re-queue all neighbors of xi (except xj)
                for xk, _ in self.constraints[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def _revise(self, domains, xi, xj):
        """Remove values from domains[xi] with no support in domains[xj]."""
        revised = False
        fns_xi_xj = [fn for (nb, fn) in self.constraints[xi] if nb == xj]

        to_remove = []
        for val_i in domains[xi]:
            has_support = any(
                all(fn(val_i, val_j) for fn in fns_xi_xj)
                for val_j in domains[xj]
            )
            if not has_support:
                to_remove.append(val_i)
                revised = True

        for v in to_remove:
            domains[xi].remove(v)
            self.metrics['ac3_pruned'] += 1

        return revised

    # ── MAC: Maintain Arc Consistency during backtracking ─────────────────
    def mac(self, var, domains):
        """
        Run AC-3 restricted to arcs involving var's neighbors.
        Called after assigning var to maintain arc consistency.
        """
        import copy
        local = copy.deepcopy(domains)
        queue = deque((nb, var) for nb, _ in self.constraints[var])
        while queue:
            xi, xj = queue.popleft()
            if self._revise(local, xi, xj):
                if len(local[xi]) == 0:
                    return None
                for xk, _ in self.constraints[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return local
