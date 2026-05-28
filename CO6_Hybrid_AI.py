# ---------------------------------------------------------
# CO6 - Hybrid AI System
# University Timetable Reasoning Engine
# Integrates: Search (CO2) + CSP (CO3) +
#             Decision Making (CO4) + Probabilistic (CO5)
# ---------------------------------------------------------

import heapq
import random

# ---------------------------------------------------------
# University Configuration
# ---------------------------------------------------------

university = {

    "departments": [
        "Science",
        "Arts",
        "Engineering"
    ]
}

# ---------------------------------------------------------
# Course Database
# ---------------------------------------------------------

courses = {

    "Mathematics": {
        "faculty":         "Dr. Sharma",
        "required_type":   "Lecture Hall",
        "capacity_needed": 60,
        "conflict_prob":   0.40,
        "cost":            2,
        "treatments":      ["Morning Slot", "Midday Slot"]
    },

    "Physics": {
        "faculty":         "Dr. Rao",
        "required_type":   "Lab",
        "capacity_needed": 30,
        "conflict_prob":   0.50,
        "cost":            4,
        "treatments":      ["Morning Slot"]
    },

    "Computer Science": {
        "faculty":         "Dr. Mehta",
        "required_type":   "Computer Lab",
        "capacity_needed": 40,
        "conflict_prob":   0.30,
        "cost":            1,
        "treatments":      ["Morning Slot", "Afternoon Slot"]
    },

    "Chemistry": {
        "faculty":         "Dr. Nair",
        "required_type":   "Lab",
        "capacity_needed": 35,
        "conflict_prob":   0.45,
        "cost":            3,
        "treatments":      ["Midday Slot"]
    },

    "English": {
        "faculty":         "Dr. Kapoor",
        "required_type":   "Classroom",
        "capacity_needed": 50,
        "conflict_prob":   0.20,
        "cost":            2,
        "treatments":      ["Morning Slot", "Midday Slot", "Afternoon Slot"]
    }
}

# ---------------------------------------------------------
# Room Database
# ---------------------------------------------------------

rooms = {
    "Lecture Hall A": {"type": "Lecture Hall", "capacity": 80},
    "Lab 101":        {"type": "Lab",          "capacity": 40},
    "Computer Lab B": {"type": "Computer Lab", "capacity": 45},
    "Classroom 201":  {"type": "Classroom",    "capacity": 60}
}

TIME_SLOTS = [
    "Monday 9AM",
    "Monday 11AM",
    "Tuesday 9AM",
    "Tuesday 11AM",
    "Wednesday 9AM"
]

# ---------------------------------------------------------
# Explainability Logs
# ---------------------------------------------------------

logs = []

# ---------------------------------------------------------
# CO2 - HEURISTIC + A* SEARCH
# Schedules courses by f(n) = cost + capacity gap
# ---------------------------------------------------------

def heuristic(capacity_needed):

    ideal = 100

    return abs(ideal - capacity_needed)

def a_star_search():

    print("\nA* SEARCH RESULTS:\n")

    priority_queue = []

    slot_index = 0

    for course, info in courses.items():

        g = info["cost"]

        h = heuristic(info["capacity_needed"])

        f = g + h

        heapq.heappush(
            priority_queue,
            (f, course)
        )

    results = []

    while priority_queue:

        score, course = heapq.heappop(priority_queue)

        slot = (
            TIME_SLOTS[slot_index]
            if slot_index < len(TIME_SLOTS)
            else "No Slot Available"
        )

        slot_index += 1

        print(
            f"{course:<20} -> "
            f"f(n) = {score:<5} | "
            f"Proposed Slot: {slot}"
        )

        results.append((course, slot))

    return results

# ---------------------------------------------------------
# CO3 - CSP CONSTRAINT CHECKING
# Ensures no faculty or room clash
# ---------------------------------------------------------

def is_valid_assignment(course, slot, room_name, assignment):

    for assigned_course, assigned_slot, assigned_room in assignment:

        # Same slot?

        if assigned_slot == slot:

            # Room clash

            if assigned_room == room_name:

                logs.append(
                    f"Room clash: {course} and "
                    f"{assigned_course} both need "
                    f"{room_name} at {slot}"
                )

                return False

            # Faculty clash

            if (
                courses[course]["faculty"]
                == courses[assigned_course]["faculty"]
            ):

                logs.append(
                    f"Faculty clash: "
                    f"{courses[course]['faculty']} "
                    f"cannot teach both {course} and "
                    f"{assigned_course} at {slot}"
                )

                return False

    return True

def forward_checking():

    print("\nFORWARD CHECKING (CSP):\n")

    assignment = []

    slot_index = 0

    for course, info in courses.items():

        assigned = False

        for slot in TIME_SLOTS:

            for room_name, room_info in rooms.items():

                type_ok = (
                    room_info["type"] == info["required_type"]
                )

                cap_ok = (
                    room_info["capacity"] >= info["capacity_needed"]
                )

                if (
                    type_ok
                    and cap_ok
                    and is_valid_assignment(
                        course, slot, room_name, assignment
                    )
                ):

                    assignment.append(
                        (course, slot, room_name)
                    )

                    logs.append(
                        f"CSP Assigned: {course} -> "
                        f"Slot: {slot}, Room: {room_name}"
                    )

                    print(
                        f"{course:<20} | "
                        f"Slot: {slot:<20} | "
                        f"Room: {room_name}"
                    )

                    assigned = True

                    break

            if assigned:
                break

        if not assigned:

            logs.append(
                f"CSP Failed: No valid slot+room for {course}"
            )

            print(f"{course:<20} | FAILED: No valid assignment")

    return assignment

# ---------------------------------------------------------
# CO5 - BAYESIAN CONFLICT PROBABILITY
# Estimates how likely each course causes a conflict
# ---------------------------------------------------------

def bayesian_reasoning():

    print("\nBAYESIAN CONFLICT PROBABILITIES:\n")

    results = {}

    for course, info in courses.items():

        prior = info["conflict_prob"]

        # Likelihood = capacity pressure

        likelihood = info["capacity_needed"] / 100

        evidence = 0.50

        posterior = (likelihood * prior) / evidence

        results[course] = round(posterior, 2)

        print(
            f"{course:<20} -> "
            f"Conflict Probability = {posterior:.2f}"
        )

    return results

# ---------------------------------------------------------
# CO4 - UTILITY FUNCTION + DECISION MAKING
# Scores each course for scheduling priority
# ---------------------------------------------------------

def utility_function(conflict_prob, slot_count):

    utility = (
        (1 - conflict_prob) * 100
        - slot_count * 3
    )

    return utility

def select_best_decision(probabilities):

    print("\nDECISION MAKING (Utility Scores):\n")

    best_course = None

    best_utility = -999

    for course, prob in probabilities.items():

        slot_count = len(courses[course]["treatments"])

        utility = utility_function(prob, slot_count)

        print(
            f"{course:<20} -> "
            f"Utility = {utility:.2f}"
        )

        if utility > best_utility:

            best_utility = utility
            best_course = course

    return best_course

# ---------------------------------------------------------
# CO6 - EXPLAINABILITY
# ---------------------------------------------------------

def explain_result(final_course, csp_assignment):

    print("\nEXPLAINABILITY:\n")

    print(f"Highest Priority Course: {final_course}")

    print("\nCourse Details:")

    info = courses[final_course]

    print(f"  Faculty         : {info['faculty']}")
    print(f"  Room Type Needed: {info['required_type']}")
    print(f"  Capacity Needed : {info['capacity_needed']}")
    print(f"  Conflict Risk   : {info['conflict_prob']}")

    print("\nFull Timetable (CSP Assignments):")

    for course, slot, room in csp_assignment:

        print(
            f"  {course:<20} | "
            f"{slot:<20} | "
            f"{room}"
        )

    print("\nCSP & Agent Reasoning Logs:")

    for log in logs:

        print(f"  {log}")

# ---------------------------------------------------------
# FAILURE ANALYSIS
# ---------------------------------------------------------

def failure_analysis():

    print("\nFAILURE ANALYSIS:\n")

    print("- Limited room database may cause unscheduled courses")
    print("- Simplified probability model ignores semester patterns")
    print("- No real university dataset used for training")
    print("- Dynamic course additions not yet supported")

# ---------------------------------------------------------
# ETHICS & LIMITATIONS
# ---------------------------------------------------------

def ethics_and_limitations():

    print("\nETHICS & LIMITATIONS:\n")

    print("- AI scheduling may favour certain departments unintentionally")
    print("- Faculty preferences are not fully modelled")
    print("- Accessibility needs (e.g. wheelchair rooms) not considered")
    print("- Not suitable for direct deployment without human review")

# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------

print("========================================")
print("UNIVERSITY TIMETABLE REASONING ENGINE")
print("CO6 - HYBRID AI SYSTEM")
print("========================================")

# ---------------------------------------------------------
# CO2 - A* Search
# ---------------------------------------------------------

print("\n--- CO2: A* SEARCH ---")

search_results = a_star_search()

# ---------------------------------------------------------
# CO3 - CSP Forward Checking
# ---------------------------------------------------------

print("\n--- CO3: CSP FORWARD CHECKING ---")

csp_assignment = forward_checking()

# ---------------------------------------------------------
# CO5 - Bayesian Reasoning
# ---------------------------------------------------------

print("\n--- CO5: BAYESIAN REASONING ---")

probability_results = bayesian_reasoning()

# ---------------------------------------------------------
# CO4 - Decision Making
# ---------------------------------------------------------

print("\n--- CO4: DECISION MAKING ---")

final_course = select_best_decision(probability_results)

print(
    f"\nHighest Priority Course: {final_course}"
)

# ---------------------------------------------------------
# CO6 - Explainability
# ---------------------------------------------------------

explain_result(final_course, csp_assignment)

# ---------------------------------------------------------
# Performance Summary
# ---------------------------------------------------------

print("\nPERFORMANCE SUMMARY:\n")

print(
    f"Courses Processed     : {len(courses)}"
)

print(
    f"Courses Scheduled     : {len(csp_assignment)}"
)

print(
    f"Courses Failed        : "
    f"{len(courses) - len(csp_assignment)}"
)

print(
    f"Rooms Available       : {len(rooms)}"
)

print(
    f"Time Slots Available  : {len(TIME_SLOTS)}"
)

# ---------------------------------------------------------
# Failure Analysis
# ---------------------------------------------------------

failure_analysis()

# ---------------------------------------------------------
# Ethics & Limitations
# ---------------------------------------------------------

ethics_and_limitations()

print("\n========================================")
print("HYBRID AI PROCESS COMPLETED")
print("========================================")
