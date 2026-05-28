# ---------------------------------------------------------
# CO4 - Decision Making & Game Reasoning
# University Timetable Reasoning Engine
# ---------------------------------------------------------

import math
import random

# ---------------------------------------------------------
# Timetable Slot Options
# Each slot option is evaluated for scheduling utility
# ---------------------------------------------------------

slot_options = {

    "Morning Slot": {
        "faculty_preference": 85,
        "student_attendance": 90,
        "room_availability": 95,
        "conflict_risk": 10
    },

    "Midday Slot": {
        "faculty_preference": 70,
        "student_attendance": 75,
        "room_availability": 80,
        "conflict_risk": 20
    },

    "Afternoon Slot": {
        "faculty_preference": 60,
        "student_attendance": 65,
        "room_availability": 70,
        "conflict_risk": 30
    }
}

# ---------------------------------------------------------
# Course Scheduling Priority Data
# ---------------------------------------------------------

course_priorities = {

    "Mathematics": {
        "enrollment": 60,
        "lab_required": False,
        "scheduling_cost": 2
    },

    "Physics": {
        "enrollment": 30,
        "lab_required": True,
        "scheduling_cost": 4
    },

    "Computer Science": {
        "enrollment": 40,
        "lab_required": True,
        "scheduling_cost": 1
    }
}

# ---------------------------------------------------------
# Utility Function
# Utility = Preference + Attendance + Availability - Risk
# ---------------------------------------------------------

def utility_function(faculty_preference,
                     student_attendance,
                     room_availability,
                     conflict_risk):

    utility = (
        faculty_preference
        + student_attendance
        + room_availability
        - (conflict_risk * 1.5)
    )

    return utility

# ---------------------------------------------------------
# Evaluation Function
# ---------------------------------------------------------

def evaluate_slot(slot_name):

    data = slot_options[slot_name]

    score = utility_function(
        data["faculty_preference"],
        data["student_attendance"],
        data["room_availability"],
        data["conflict_risk"]
    )

    return score

# ---------------------------------------------------------
# Minimax Algorithm
# Timetable Coordinator (MAX) vs. Conflict Generator (MIN)
# MAX = tries to schedule for best outcome
# MIN = simulates worst-case clashes
# ---------------------------------------------------------

def minimax(depth,
            maximizing_player,
            slot_list):

    if depth == 0 or len(slot_list) == 0:

        return 0

    if maximizing_player:

        best_value = -math.inf

        for slot in slot_list:

            value = evaluate_slot(slot)

            value += minimax(
                depth - 1,
                False,
                []
            )

            best_value = max(best_value, value)

        return best_value

    else:

        worst_value = math.inf

        for slot in slot_list:

            value = evaluate_slot(slot)

            value -= minimax(
                depth - 1,
                True,
                []
            )

            worst_value = min(worst_value, value)

        return worst_value

# ---------------------------------------------------------
# Alpha-Beta Pruning
# Optimizes Minimax by pruning unnecessary branches
# ---------------------------------------------------------

def alpha_beta(depth,
               alpha,
               beta,
               maximizing_player,
               slot_list):

    if depth == 0 or len(slot_list) == 0:

        return 0

    if maximizing_player:

        value = -math.inf

        for slot in slot_list:

            score = evaluate_slot(slot)

            value = max(value, score)

            alpha = max(alpha, value)

            if beta <= alpha:

                print(
                    f"  Beta Cutoff at slot: {slot}"
                )

                break

        return value

    else:

        value = math.inf

        for slot in slot_list:

            score = evaluate_slot(slot)

            value = min(value, score)

            beta = min(beta, value)

            if beta <= alpha:

                print(
                    f"  Alpha Cutoff at slot: {slot}"
                )

                break

        return value

# ---------------------------------------------------------
# Policy Selection
# Picks the best scheduling slot
# ---------------------------------------------------------

def select_best_policy():

    best_slot = None

    best_score = -math.inf

    for slot in slot_options:

        score = evaluate_slot(slot)

        print(
            f"{slot:<20} "
            f"Utility Score = {score:.2f}"
        )

        if score > best_score:

            best_score = score
            best_slot = slot

    return best_slot, best_score

# ---------------------------------------------------------
# Iterative Deepening
# Progressively deeper scheduling search
# ---------------------------------------------------------

def iterative_deepening(max_depth):

    print("\nIterative Deepening Search:\n")

    for depth in range(1, max_depth + 1):

        score = minimax(
            depth,
            True,
            list(slot_options.keys())
        )

        print(
            f"Depth {depth} "
            f"-> Best Score: {score:.2f}"
        )

# ---------------------------------------------------------
# Expectimax
# Stochastic decision: accounts for uncertain attendance
# ---------------------------------------------------------

def expectimax():

    expected_values = {}

    for slot, data in slot_options.items():

        success_prob = data["student_attendance"] / 100

        failure_prob = 1 - success_prob

        expected_utility = (

            success_prob * data["faculty_preference"]

            -

            failure_prob * data["conflict_risk"]

        )

        expected_values[slot] = expected_utility

    return expected_values

# ---------------------------------------------------------
# Bounded Rationality
# Quick slot selection under time pressure
# ---------------------------------------------------------

def bounded_rationality():

    quick_choice = random.choice(
        list(slot_options.keys())
    )

    return quick_choice

# ---------------------------------------------------------
# Multi-Agent Reasoning
# Faculty agent vs Student agent vs Admin agent
# ---------------------------------------------------------

def multi_agent_reasoning():

    faculty_agent = "Morning Slot"

    student_agent = "Midday Slot"

    admin_agent   = "Morning Slot"

    print("Faculty Agent Preference  :", faculty_agent)
    print("Student Agent Preference  :", student_agent)
    print("Admin Agent Preference    :", admin_agent)

    # Voting-based final decision

    votes = {
        faculty_agent: 0,
        student_agent: 0,
        admin_agent:   0
    }

    votes[faculty_agent] += 1
    votes[student_agent] += 1
    votes[admin_agent]   += 1

    final_decision = max(votes, key=votes.get)

    return final_decision

# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

print("========================================")
print("UNIVERSITY TIMETABLE REASONING ENGINE")
print("CO4 - DECISION MAKING MODULE")
print("========================================")

# ---------------------------------------------------------
# Utility Scores
# ---------------------------------------------------------

print("\nSlot Utility Scores:\n")

for slot in slot_options:

    score = evaluate_slot(slot)

    print(
        f"{slot:<20} -> "
        f"Utility Score = {score:.2f}"
    )

# ---------------------------------------------------------
# Best Policy
# ---------------------------------------------------------

print("\nBest Slot Policy:\n")

best_slot, best_score = select_best_policy()

print(
    f"\nSelected Slot  : {best_slot}"
)

print(
    f"Best Score     : {best_score:.2f}"
)

# ---------------------------------------------------------
# Minimax
# ---------------------------------------------------------

print("\nMinimax Result:\n")

minimax_score = minimax(
    2,
    True,
    list(slot_options.keys())
)

print(
    f"Minimax Score = {minimax_score:.2f}"
)

# ---------------------------------------------------------
# Alpha-Beta Pruning
# ---------------------------------------------------------

print("\nAlpha-Beta Result:\n")

ab_score = alpha_beta(
    2,
    -math.inf,
    math.inf,
    True,
    list(slot_options.keys())
)

print(
    f"Alpha-Beta Score = {ab_score:.2f}"
)

# ---------------------------------------------------------
# Iterative Deepening
# ---------------------------------------------------------

iterative_deepening(3)

# ---------------------------------------------------------
# Expectimax
# ---------------------------------------------------------

print("\nExpectimax Expected Utilities:\n")

expectimax_result = expectimax()

for slot, value in expectimax_result.items():

    print(
        f"{slot:<20} -> "
        f"Expected Utility = {value:.2f}"
    )

# ---------------------------------------------------------
# Bounded Rationality
# ---------------------------------------------------------

print("\nBounded Rationality Decision:\n")

quick_decision = bounded_rationality()

print(
    f"Quick Slot Selected: {quick_decision}"
)

# ---------------------------------------------------------
# Multi-Agent Reasoning
# ---------------------------------------------------------

print("\nMulti-Agent Reasoning:\n")

final_slot = multi_agent_reasoning()

print(
    f"\nFinal Agreed Slot: {final_slot}"
)

print("\n========================================")
print("DECISION PROCESS COMPLETED")
print("========================================")
