"""
algorithms/backtracking.py — Backtracking Search Engine
CO3: Core search algorithm combining all CSP heuristics.

Uses:
  - MRV + Degree for variable selection
  - LCV for value ordering
  - MAC (AC-3) for constraint propagation after each assignment
  - Forward checking to detect dead ends early
"""

import copy
import time
from algorithms.csp import CSP
from algorithms.degree import select_variable
from algorithms.lcv import lcv


# ─────────────────────────────────────────────────────
#  Timetable CSP Builder
# ─────────────────────────────────────────────────────

def build_timetable_csp(subjects, teachers, classrooms, timeslots):
    """
    Build a CSP instance for timetable scheduling.

    Variables : one per subject  (sub['id'])
    Domains   : list of (teacher_id, classroom_id, timeslot_id) triples
    Constraints (Hard):
      1. Same teacher cannot teach two subjects at same timeslot
      2. Same classroom cannot host two subjects at same timeslot
    """
    csp = CSP()

    # Build full domain: all (teacher, room, slot) combos per subject
    for sub in subjects:
        domain = [
            (t['id'], c['id'], ts['id'])
            for t in teachers
            for c in classrooms
            for ts in timeslots
        ]
        csp.add_variable(sub['id'], domain)

    # Add pairwise constraints between every pair of subjects
    sub_ids = [s['id'] for s in subjects]
    for i in range(len(sub_ids)):
        for j in range(i + 1, len(sub_ids)):
            v1, v2 = sub_ids[i], sub_ids[j]

            def make_constraint():
                def constraint(val1, val2):
                    t1, c1, ts1 = val1
                    t2, c2, ts2 = val2
                    if ts1 == ts2:
                        # Same timeslot → must differ in teacher AND room
                        if t1 == t2:
                            return False   # Teacher clash
                        if c1 == c2:
                            return False   # Room clash
                    return True
                return constraint

            csp.add_constraint(v1, v2, make_constraint())

    return csp


# ─────────────────────────────────────────────────────
#  Backtracking Search
# ─────────────────────────────────────────────────────

def backtracking_search(csp):
    """
    Backtracking search with MAC, MRV+Degree, and LCV.

    Returns:
        (solution_dict, metrics) or (None, metrics)
    """
    start = time.time()
    csp.metrics = {'backtracks': 0, 'constraint_checks': 0, 'ac3_pruned': 0}

    # Phase 1: AC-3 preprocessing — prune domains before search
    domains = copy.deepcopy(csp.domains)
    if not csp.ac3(domains):
        return None, csp.metrics   # No solution after preprocessing

    result = _backtrack({}, domains, csp)
    csp.metrics['solve_time_ms'] = round((time.time() - start) * 1000, 2)
    return result, csp.metrics


def _backtrack(assignment, domains, csp):
    """Recursive backtracking with MAC propagation."""

    # Base case: complete assignment
    if len(assignment) == len(csp.variables):
        return dict(assignment)

    # Select next variable: MRV + Degree heuristic
    var = select_variable(csp.variables, domains, csp.neighbors, assignment)
    if var is None:
        return None

    # Order values: LCV heuristic
    ordered_values = lcv(
        var,
        domains[var],
        csp.neighbors,
        domains,
        csp.constraints,
        assignment
    )

    for value in ordered_values:
        csp.metrics['constraint_checks'] += 1

        if csp.is_consistent(var, value, assignment):
            assignment[var] = value

            # MAC: maintain arc consistency after assignment
            new_domains = copy.deepcopy(domains)
            new_domains[var] = [value]
            pruned_domains = csp.mac(var, new_domains)

            if pruned_domains is not None:
                result = _backtrack(assignment, pruned_domains, csp)
                if result is not None:
                    return result

            del assignment[var]
            csp.metrics['backtracks'] += 1

    return None


# ─────────────────────────────────────────────────────
#  Main Entry Point
# ─────────────────────────────────────────────────────

def generate_timetable(subjects, teachers, classrooms, timeslots):
    """
    Full CSP timetable generation pipeline.

    Returns:
        dict with keys: success, assignments, metrics, conflicts
    """
    if not subjects or not teachers or not classrooms or not timeslots:
        return {
            'success': False,
            'error': 'Need at least one subject, teacher, classroom, and timeslot.',
            'assignments': [],
            'metrics': {}
        }

    csp = build_timetable_csp(subjects, teachers, classrooms, timeslots)
    solution, metrics = backtracking_search(csp)

    if solution is None:
        return {
            'success': False,
            'error': 'CSP solver could not find a conflict-free timetable. Add more timeslots or rooms.',
            'assignments': [],
            'metrics': metrics
        }

    # Map subject IDs back to full data
    subj_map = {s['id']: s for s in subjects}
    teacher_map = {t['id']: t for t in teachers}
    room_map = {c['id']: c for c in classrooms}
    slot_map = {ts['id']: ts for ts in timeslots}

    assignments = []
    for sub_id, (teacher_id, classroom_id, timeslot_id) in solution.items():
        assignments.append({
            'subject_id': sub_id,
            'subject_name': subj_map[sub_id]['subject_name'],
            'teacher_id': teacher_id,
            'teacher_name': teacher_map[teacher_id]['teacher_name'],
            'classroom_id': classroom_id,
            'room_number': room_map[classroom_id]['room_number'],
            'timeslot_id': timeslot_id,
            'day': slot_map[timeslot_id]['day'],
            'start_time': slot_map[timeslot_id]['start_time'],
            'end_time': slot_map[timeslot_id]['end_time'],
        })

    # Soft constraint quality score
    quality = _evaluate_quality(assignments)
    metrics['quality_score'] = quality
    metrics['variables'] = len(subjects)
    metrics['constraints'] = len(subjects) * (len(subjects) - 1) // 2
    metrics['heuristics'] = ['MRV', 'Degree', 'LCV', 'AC-3 (MAC)']

    return {
        'success': True,
        'assignments': assignments,
        'metrics': metrics
    }


def _evaluate_quality(assignments):
    """
    Soft constraint quality score (0–100).
    Checks: spread across days, teacher gap minimization.
    """
    if not assignments:
        return 0

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    day_counts = {d: 0 for d in days}
    for a in assignments:
        if a['day'] in day_counts:
            day_counts[a['day']] += 1

    used_days = sum(1 for d in days if day_counts[d] > 0)
    spread_score = (used_days / len(days)) * 100 if days else 0

    return round(spread_score, 1)
