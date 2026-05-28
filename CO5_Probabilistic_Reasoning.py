# ---------------------------------------------------------
# CO5 - Probabilistic Reasoning
# University Timetable Reasoning Engine
# ---------------------------------------------------------

import random

# ---------------------------------------------------------
# Department Request
# Which departments need scheduling
# ---------------------------------------------------------

department_request = {
    "departments": [
        "Science",
        "Arts",
        "Engineering"
    ]
}

# ---------------------------------------------------------
# Prior Probabilities
# P(Scheduling Conflict | Department)
# ---------------------------------------------------------

conflict_priors = {
    "Science":     0.40,
    "Arts":        0.20,
    "Engineering": 0.50
}

# ---------------------------------------------------------
# Likelihood
# P(Symptom = Overlap | Department)
# Overlap = faculty or room being double-booked
# ---------------------------------------------------------

likelihoods = {
    "Science":     0.70,
    "Arts":        0.30,
    "Engineering": 0.80
}

# ---------------------------------------------------------
# Evidence
# P(Overlap observed across all departments)
# ---------------------------------------------------------

evidence = 0.55

# ---------------------------------------------------------
# Bayesian Network
# Department -> Typical Conflict Triggers
# ---------------------------------------------------------

bayesian_network = {

    "Science": [
        "lab_double_booking",
        "faculty_clash",
        "peak_hour_demand"
    ],

    "Arts": [
        "room_unavailability"
    ],

    "Engineering": [
        "lab_double_booking",
        "faculty_clash",
        "room_unavailability",
        "peak_hour_demand"
    ]
}

# ---------------------------------------------------------
# Observed Conflict Triggers
# ---------------------------------------------------------

observed_triggers = [
    "lab_double_booking",
    "faculty_clash"
]

# ---------------------------------------------------------
# Bayes Theorem
# P(Conflict | Evidence) = P(E|C) * P(C) / P(E)
# ---------------------------------------------------------

def bayes_theorem(prior, likelihood, evidence):

    posterior = (likelihood * prior) / evidence

    return posterior

# ---------------------------------------------------------
# Bayesian Inference
# ---------------------------------------------------------

def bayesian_inference():

    print("\nBayesian Inference Results:\n")

    results = {}

    for dept in conflict_priors:

        prior = conflict_priors[dept]

        likelihood = likelihoods[dept]

        posterior = bayes_theorem(
            prior,
            likelihood,
            evidence
        )

        results[dept] = posterior

        print(
            f"{dept:<15} -> "
            f"Conflict Probability = {posterior:.2f}"
        )

    return results

# ---------------------------------------------------------
# Variable Elimination
# Marginalise out hidden variable: room_demand
# ---------------------------------------------------------

def variable_elimination():

    print("\nVariable Elimination:\n")

    hidden_variable = "room_demand"

    print(
        f"Eliminating hidden variable: "
        f"{hidden_variable}"
    )

    probability = 0

    for dept in conflict_priors:

        probability += (
            conflict_priors[dept]
            * likelihoods[dept]
        )

    print(
        f"Combined Conflict Probability = "
        f"{probability:.2f}"
    )

# ---------------------------------------------------------
# Belief Propagation
# Score each department by how many triggers match
# ---------------------------------------------------------

def belief_propagation():

    print("\nBelief Propagation:\n")

    for dept, triggers in bayesian_network.items():

        matched = 0

        for trigger in triggers:

            if trigger in observed_triggers:

                matched += 1

        belief = matched / len(triggers)

        print(
            f"{dept:<15} Belief Score = "
            f"{belief:.2f}"
        )

# ---------------------------------------------------------
# Rejection Sampling
# Estimate conflict probability by sampling
# ---------------------------------------------------------

def rejection_sampling(samples=1000):

    print("\nRejection Sampling:\n")

    accepted = 0

    for i in range(samples):

        sample = random.random()

        if sample < 0.50:

            accepted += 1

    probability = accepted / samples

    print(
        f"Estimated Conflict Probability = "
        f"{probability:.2f}"
    )

# ---------------------------------------------------------
# Likelihood Weighting
# Weighted estimate of scheduling difficulty
# ---------------------------------------------------------

def likelihood_weighting(samples=1000):

    print("\nLikelihood Weighting:\n")

    weighted_sum = 0

    total_weight = 0

    for i in range(samples):

        weight = random.uniform(0.4, 1.0)

        weighted_sum += weight

        total_weight += 1

    estimate = weighted_sum / total_weight

    print(
        f"Weighted Scheduling Difficulty = "
        f"{estimate:.2f}"
    )

# ---------------------------------------------------------
# Markov Chain
# Day-by-day timetable state transitions
# ---------------------------------------------------------

def markov_chain(steps=5):

    print("\nMarkov Chain (Daily State):\n")

    states = [
        "Conflict-Free",
        "Has Conflict"
    ]

    current_state = "Conflict-Free"

    for step in range(steps):

        print(
            f"Day {step + 1}: "
            f"{current_state}"
        )

        if current_state == "Conflict-Free":

            current_state = random.choice(
                ["Conflict-Free", "Has Conflict"]
            )

        else:

            current_state = random.choice(
                ["Has Conflict", "Conflict-Free"]
            )

# ---------------------------------------------------------
# Hidden Markov Model (HMM) Intuition
# Hidden = actual schedule state
# Observed = reported issues from students/faculty
# ---------------------------------------------------------

def hmm_tracking():

    print("\nHidden Markov Model Tracking:\n")

    hidden_states = [
        "Conflict-Free",
        "Clash Detected"
    ]

    observations = [
        "No Complaints",
        "Faculty Absent",
        "Room Empty",
        "Students Confused"
    ]

    for i in range(5):

        hidden = random.choice(hidden_states)

        observed = random.choice(observations)

        print(
            f"Hidden State = {hidden:<20} | "
            f"Observation = {observed}"
        )

# ---------------------------------------------------------
# Sensor Fusion
# Combine multiple signals for scheduling quality
# ---------------------------------------------------------

def sensor_fusion():

    print("\nSensor Fusion:\n")

    room_utilisation  = 85  # percent
    faculty_load      = 4   # courses per week
    student_feedback  = 72  # satisfaction score

    print(f"Room Utilisation   = {room_utilisation}%")
    print(f"Faculty Load       = {faculty_load} courses/week")
    print(f"Student Feedback   = {student_feedback}/100")

    if (
        room_utilisation > 80
        and faculty_load > 3
    ):

        print(
            "Warning: High scheduling pressure detected. "
            "Conflict risk is elevated."
        )

    else:

        print("Scheduling load is within acceptable limits.")

# ---------------------------------------------------------
# Expected Utility
# ---------------------------------------------------------

def expected_utility():

    print("\nExpected Utility of Scheduling Strategies:\n")

    strategies = {

        "Automated CSP Solver": {
            "success_probability": 0.92,
            "utility": 100
        },

        "Manual Scheduling": {
            "success_probability": 0.60,
            "utility": 70
        },

        "Random Assignment": {
            "success_probability": 0.30,
            "utility": 40
        }
    }

    for strategy, data in strategies.items():

        expected_value = (
            data["success_probability"]
            * data["utility"]
        )

        print(
            f"{strategy:<25} -> "
            f"Expected Utility = {expected_value:.2f}"
        )

# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

print("========================================")
print("UNIVERSITY TIMETABLE REASONING ENGINE")
print("CO5 - PROBABILISTIC REASONING")
print("========================================")

# ---------------------------------------------------------
# Bayes Theorem
# ---------------------------------------------------------

print("\nBayes Theorem:\n")

bayesian_results = bayesian_inference()

# ---------------------------------------------------------
# Bayesian Network
# ---------------------------------------------------------

print("\nBayesian Network:\n")

for dept, triggers in bayesian_network.items():

    print(f"{dept} -> {triggers}")

# ---------------------------------------------------------
# Variable Elimination
# ---------------------------------------------------------

variable_elimination()

# ---------------------------------------------------------
# Belief Propagation
# ---------------------------------------------------------

belief_propagation()

# ---------------------------------------------------------
# Rejection Sampling
# ---------------------------------------------------------

rejection_sampling()

# ---------------------------------------------------------
# Likelihood Weighting
# ---------------------------------------------------------

likelihood_weighting()

# ---------------------------------------------------------
# Markov Chain
# ---------------------------------------------------------

markov_chain()

# ---------------------------------------------------------
# HMM Tracking
# ---------------------------------------------------------

hmm_tracking()

# ---------------------------------------------------------
# Sensor Fusion
# ---------------------------------------------------------

sensor_fusion()

# ---------------------------------------------------------
# Expected Utility
# ---------------------------------------------------------

expected_utility()

print("\n========================================")
print("PROBABILISTIC REASONING COMPLETED")
print("========================================")
