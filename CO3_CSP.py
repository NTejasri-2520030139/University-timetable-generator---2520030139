# ---------------------------------------------------------
# CO3 - Constraint Satisfaction Problem (CSP)
# University Timetable Reasoning Engine
# Course schedules generated without clashes,
# honoring faculty, room, and capacity constraints.
# ---------------------------------------------------------

import random

# ---------------------------------------------------------
# University Resources
# ---------------------------------------------------------

TIME_SLOTS = [
    "Monday 9AM",
    "Monday 11AM",
    "Tuesday 9AM",
    "Tuesday 11AM",
    "Wednesday 9AM",
    "Wednesday 11AM",
    "Thursday 9AM",
    "Thursday 11AM"
]

ROOMS = {
    "Lecture Hall A": {"type": "Lecture Hall", "capacity": 80},
    "Lab 101":        {"type": "Lab",          "capacity": 40},
    "Computer Lab B": {"type": "Computer Lab", "capacity": 45},
    "Classroom 201":  {"type": "Classroom",    "capacity": 60},
    "Classroom 202":  {"type": "Classroom",    "capacity": 55}
}

# ---------------------------------------------------------
# Course Variables and Their Domains
# Domain = list of (time_slot, room) pairs
# ---------------------------------------------------------

COURSES = {
    "Mathematics": {
        "faculty":           "Dr. Sharma",
        "required_type":     "Lecture Hall",
        "capacity_needed":   60
    },
    "Physics": {
        "faculty":           "Dr. Rao",
        "required_type":     "Lab",
        "capacity_needed":   30
    },
    "Computer Science": {
        "faculty":           "Dr. Mehta",
        "required_type":     "Computer Lab",
        "capacity_needed":   40
    },
    "Chemistry": {
        "faculty":           "Dr. Nair",
        "required_type":     "Lab",
        "capacity_needed":   35
    },
    "English": {
        "faculty":           "Dr. Kapoor",
        "required_type":     "Classroom",
        "capacity_needed":   50
    }
}

# ---------------------------------------------------------
# Explainability Logs
# ---------------------------------------------------------

explanation_logs = []

# ---------------------------------------------------------
# Domain Builder
# Builds valid (time_slot, room) pairs per course
# ---------------------------------------------------------

def build_domains():

    domains = {}

    for course, info in COURSES.items():

        valid_pairs = []

        for slot in TIME_SLOTS:

            for room_name, room_info in ROOMS.items():

                type_ok = (
                    room_info["type"] == info["required_type"]
                )

                capacity_ok = (
                    room_info["capacity"] >= info["capacity_needed"]
                )

                if type_ok and capacity_ok:

                    valid_pairs.append((slot, room_name))

        domains[course] = valid_pairs

    return domains

# ---------------------------------------------------------
# Constraint Checker
# No two courses can share the same time slot OR room
# No faculty can be in two courses at the same time
# ---------------------------------------------------------

def is_consistent(course, value, assignment):

    slot, room = value

    for assigned_course, assigned_value in assignment.items():

        assigned_slot, assigned_room = assigned_value

        # Time Slot Clash Check

        if slot == assigned_slot:

            # Room Clash

            if room == assigned_room:

                explanation_logs.append(
                    f"Room clash: {course} and "
                    f"{assigned_course} both need "
                    f"{room} at {slot}"
                )

                return False

            # Faculty Clash

            if (
                COURSES[course]["faculty"]
                == COURSES[assigned_course]["faculty"]
            ):

                explanation_logs.append(
                    f"Faculty clash: "
                    f"{COURSES[course]['faculty']} "
                    f"cannot teach {course} and "
                    f"{assigned_course} both at {slot}"
                )

                return False

    return True

# ---------------------------------------------------------
# Forward Checking
# Removes values from other domains that conflict
# ---------------------------------------------------------

def forward_checking(course, value, domains, assignment):

    slot, room = value

    reduced_domains = {}

    for other_course, other_values in domains.items():

        if other_course == course:
            continue

        reduced = []

        for other_value in other_values:

            other_slot, other_room = other_value

            # Would there be a room clash?

            room_clash = (
                other_slot == slot
                and other_room == room
            )

            # Would there be a faculty clash?

            faculty_clash = (
                other_slot == slot
                and COURSES[other_course]["faculty"]
                == COURSES[course]["faculty"]
            )

            if not room_clash and not faculty_clash:

                reduced.append(other_value)

            else:

                explanation_logs.append(
                    f"Forward Checking: Removed "
                    f"({other_slot}, {other_room}) "
                    f"from {other_course}"
                )

        if len(reduced) == 0:

            return None  # Domain wipeout

        reduced_domains[other_course] = reduced

    return reduced_domains

# ---------------------------------------------------------
# MRV Heuristic
# Select course with smallest remaining domain
# ---------------------------------------------------------

def select_variable_mrv(domains):

    smallest_variable = None
    smallest_size = float("inf")

    for variable, domain in domains.items():

        size = len(domain)

        if size < smallest_size:

            smallest_size = size
            smallest_variable = variable

    return smallest_variable

# ---------------------------------------------------------
# Degree Heuristic
# Select course involved in most constraints
# (courses sharing faculty or room type)
# ---------------------------------------------------------

def degree_heuristic(domains):

    max_degree = -1
    selected = None

    for course in domains:

        degree = 0

        for other_course in domains:

            if other_course == course:
                continue

            # Shared faculty = constraint

            if (
                COURSES[course]["faculty"]
                == COURSES[other_course]["faculty"]
            ):
                degree += 1

            # Shared room type = constraint

            if (
                COURSES[course]["required_type"]
                == COURSES[other_course]["required_type"]
            ):
                degree += 1

        if degree > max_degree:

            max_degree = degree
            selected = course

    return selected

# ---------------------------------------------------------
# LCV Heuristic
# Order values by least constraining first
# (sorts by slot alphabetically as proxy)
# ---------------------------------------------------------

def order_values_lcv(values):

    return sorted(values, key=lambda x: x[0])

# ---------------------------------------------------------
# Backtracking Search
# Core CSP solver with MRV + LCV + Forward Checking
# ---------------------------------------------------------

def backtracking(assignment, domains):

    # Base Condition: All courses assigned

    if len(domains) == 0:

        return assignment

    # Select Variable using MRV

    course = select_variable_mrv(domains)

    # Order Values using LCV

    ordered_values = order_values_lcv(domains[course])

    for value in ordered_values:

        slot, room = value

        if is_consistent(course, value, assignment):

            # Assign Value

            assignment[course] = value

            explanation_logs.append(
                f"Assigned {course} -> "
                f"Slot: {slot}, Room: {room}"
            )

            # Forward Checking

            remaining_domains = {
                k: v for k, v in domains.items()
                if k != course
            }

            new_domains = forward_checking(
                course,
                value,
                remaining_domains,
                assignment
            )

            if new_domains is not None:

                result = backtracking(
                    assignment,
                    new_domains
                )

                if result is not None:

                    return result

            # Backtrack

            explanation_logs.append(
                f"Backtracking from {course} -> "
                f"Slot: {slot}, Room: {room}"
            )

            assignment.pop(course)

    return None

# ---------------------------------------------------------
# Min-Conflicts Local Search
# Alternative solver using iterative repair
# ---------------------------------------------------------

def min_conflicts(domains, max_steps=200):

    current_assignment = {}

    # Random Initial Assignment

    for course, values in domains.items():

        current_assignment[course] = random.choice(values)

    for step in range(max_steps):

        # Find Conflicting Courses

        conflicts = []

        for course, value in current_assignment.items():

            temp = {
                k: v for k, v in current_assignment.items()
                if k != course
            }

            if not is_consistent(course, value, temp):

                conflicts.append(course)

        if len(conflicts) == 0:

            print(
                f"Min-Conflicts solved in "
                f"{step + 1} steps."
            )

            return current_assignment

        # Pick Random Conflicting Course

        course = random.choice(conflicts)

        # Find Value with Minimum Conflicts

        best_value = None
        best_conflict_count = float("inf")

        for value in domains[course]:

            temp = {
                k: v for k, v in current_assignment.items()
                if k != course
            }

            conflict_count = 0

            for other_course, other_value in temp.items():

                if not is_consistent(
                    course,
                    value,
                    {other_course: other_value}
                ):
                    conflict_count += 1

            if conflict_count < best_conflict_count:

                best_conflict_count = conflict_count
                best_value = value

        if best_value is not None:

            current_assignment[course] = best_value

    print("Min-Conflicts: Max steps reached.")

    return current_assignment

# ---------------------------------------------------------
# SAT Check
# Logical rule: fever AND cough -> check constraints met
# ---------------------------------------------------------

def sat_check(assignment):

    has_room = all(
        v[1] is not None
        for v in assignment.values()
    )

    has_slot = all(
        v[0] is not None
        for v in assignment.values()
    )

    if has_room and has_slot:

        return "All constraints satisfied - Valid Timetable"

    return "Constraint violation detected"

# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

print("========================================")
print("UNIVERSITY TIMETABLE REASONING ENGINE")
print("CO3 - CSP MODULE")
print("========================================")

# ---------------------------------------------------------
# Build Domains
# ---------------------------------------------------------

print("\nBuilding Course Domains:\n")

domains = build_domains()

for course, values in domains.items():

    print(f"{course} -> {len(values)} valid (slot, room) pairs")

# ---------------------------------------------------------
# MRV Heuristic
# ---------------------------------------------------------

print("\nMRV Selected Course:")

mrv_course = select_variable_mrv(domains)

print(mrv_course)

# ---------------------------------------------------------
# Degree Heuristic
# ---------------------------------------------------------

print("\nDegree Heuristic Course:")

degree_course = degree_heuristic(domains)

print(degree_course)

# ---------------------------------------------------------
# Backtracking Search
# ---------------------------------------------------------

print("\nBacktracking Solution:\n")

solution = backtracking({}, domains)

if solution:

    for course, (slot, room) in solution.items():

        print(
            f"{course:<20} | "
            f"Slot: {slot:<20} | "
            f"Room: {room}"
        )

else:

    print("No solution found.")

# ---------------------------------------------------------
# Min-Conflicts Search
# ---------------------------------------------------------

print("\nMin-Conflicts Solution:\n")

domains_fresh = build_domains()

local_solution = min_conflicts(domains_fresh)

for course, (slot, room) in local_solution.items():

    print(
        f"{course:<20} | "
        f"Slot: {slot:<20} | "
        f"Room: {room}"
    )

# ---------------------------------------------------------
# SAT Logic Result
# ---------------------------------------------------------

print("\nSAT Logic Result:\n")

if solution:
    print(sat_check(solution))
else:
    print("No assignment to check.")

# ---------------------------------------------------------
# Explainability Logs
# ---------------------------------------------------------

print("\nExplainability Logs (last 10):\n")

for log in explanation_logs[-10:]:

    print(log)

print("\n========================================")
print("CSP PROCESS COMPLETED")
print("========================================")
