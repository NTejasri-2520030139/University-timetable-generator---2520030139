# ---------------------------------------------------
# CO2 - Search Algorithms Integrated System
# University Timetable Reasoning Engine
# ---------------------------------------------------

from collections import deque
import heapq
import time

# ---------------------------------------------------
# Course Database
# ---------------------------------------------------

COURSE_DATABASE = {

    "Mathematics": {
        "faculty": "Dr. Sharma",
        "room_type": "Lecture Hall",
        "capacity_needed": 60,
        "cost": 2
    },

    "Physics": {
        "faculty": "Dr. Rao",
        "room_type": "Lab",
        "capacity_needed": 30,
        "cost": 4
    },

    "Computer Science": {
        "faculty": "Dr. Mehta",
        "room_type": "Computer Lab",
        "capacity_needed": 40,
        "cost": 1
    },

    "Chemistry": {
        "faculty": "Dr. Nair",
        "room_type": "Lab",
        "capacity_needed": 35,
        "cost": 3
    },

    "English": {
        "faculty": "Dr. Kapoor",
        "room_type": "Classroom",
        "capacity_needed": 50,
        "cost": 2
    }
}

# ---------------------------------------------------
# Available Time Slots (Goal States)
# ---------------------------------------------------

AVAILABLE_SLOTS = [
    "Monday 9AM",
    "Monday 11AM",
    "Tuesday 9AM",
    "Tuesday 11AM",
    "Wednesday 9AM"
]

# ---------------------------------------------------
# Heuristic Function
# h(n) = Capacity gap from ideal room size (100)
# Lower gap = better fit
# ---------------------------------------------------

def heuristic(capacity_needed):

    ideal_capacity = 100

    gap = abs(ideal_capacity - capacity_needed)

    return gap

# ---------------------------------------------------
# BFS Search
# Visits all courses level by level
# ---------------------------------------------------

def bfs_search():

    print("\n==============================")
    print("BREADTH FIRST SEARCH (BFS)")
    print("==============================")

    start_time = time.time()

    queue = deque(COURSE_DATABASE.keys())

    visited = set()

    node_expansions = 0

    schedule_order = []

    while queue:

        course = queue.popleft()

        if course not in visited:

            visited.add(course)

            node_expansions += 1

            schedule_order.append(course)

            print(f"Visited: {course}")

    end_time = time.time()

    print(f"\nScheduling Order  : {schedule_order}")
    print(f"Node Expansions   : {node_expansions}")
    print(f"Runtime           : {end_time - start_time:.6f} seconds")

# ---------------------------------------------------
# DFS Search
# Visits courses using recursive stack
# ---------------------------------------------------

def dfs_recursive(courses, visited, node_expansions):

    if not courses:
        return node_expansions

    course = courses.pop()

    if course not in visited:

        visited.add(course)

        node_expansions += 1

        print(f"Visited: {course}")

    return dfs_recursive(
        courses,
        visited,
        node_expansions
    )

def dfs_search():

    print("\n==============================")
    print("DEPTH FIRST SEARCH (DFS)")
    print("==============================")

    start_time = time.time()

    courses = list(COURSE_DATABASE.keys())

    visited = set()

    node_expansions = dfs_recursive(
        courses,
        visited,
        0
    )

    end_time = time.time()

    print(f"\nNode Expansions   : {node_expansions}")
    print(f"Runtime           : {end_time - start_time:.6f} seconds")

# ---------------------------------------------------
# Uniform Cost Search (UCS)
# Schedules courses by lowest scheduling cost first
# ---------------------------------------------------

def ucs_search():

    print("\n==============================")
    print("UNIFORM COST SEARCH (UCS)")
    print("==============================")

    start_time = time.time()

    priority_queue = []

    visited = set()

    node_expansions = 0

    slot_index = 0

    for course, info in COURSE_DATABASE.items():

        heapq.heappush(
            priority_queue,
            (info["cost"], course)
        )

    while priority_queue:

        cost, course = heapq.heappop(priority_queue)

        if course not in visited:

            visited.add(course)

            node_expansions += 1

            slot = (
                AVAILABLE_SLOTS[slot_index]
                if slot_index < len(AVAILABLE_SLOTS)
                else "No Slot Available"
            )

            slot_index += 1

            print(
                f"Scheduled: {course:<20} | "
                f"Cost: {cost} | "
                f"Slot: {slot}"
            )

    end_time = time.time()

    print(f"\nNode Expansions   : {node_expansions}")
    print(f"Runtime           : {end_time - start_time:.6f} seconds")

# ---------------------------------------------------
# Greedy Best First Search
# Schedules course with smallest capacity gap first
# ---------------------------------------------------

def greedy_search():

    print("\n==============================")
    print("GREEDY BEST FIRST SEARCH")
    print("==============================")

    start_time = time.time()

    priority_queue = []

    visited = set()

    node_expansions = 0

    for course, info in COURSE_DATABASE.items():

        h = heuristic(info["capacity_needed"])

        heapq.heappush(
            priority_queue,
            (h, course)
        )

    while priority_queue:

        h, course = heapq.heappop(priority_queue)

        if course not in visited:

            visited.add(course)

            node_expansions += 1

            print(
                f"Visited: {course:<20} | "
                f"Heuristic (Capacity Gap): {h}"
            )

    end_time = time.time()

    print(f"\nNode Expansions   : {node_expansions}")
    print(f"Runtime           : {end_time - start_time:.6f} seconds")

# ---------------------------------------------------
# A* Search Algorithm
# f(n) = g(n) + h(n)
# g(n) = scheduling cost
# h(n) = capacity gap heuristic
# ---------------------------------------------------

def a_star_search():

    print("\n==============================")
    print("A* SEARCH")
    print("==============================")

    start_time = time.time()

    open_set = []

    closed_set = set()

    node_expansions = 0

    tie_breaker = 0

    slot_index = 0

    for course, info in COURSE_DATABASE.items():

        g = info["cost"]

        h = heuristic(info["capacity_needed"])

        f = g + h

        heapq.heappush(
            open_set,
            (f, tie_breaker, course)
        )

        tie_breaker += 1

    while open_set:

        f, _, course = heapq.heappop(open_set)

        if course not in closed_set:

            closed_set.add(course)

            node_expansions += 1

            slot = (
                AVAILABLE_SLOTS[slot_index]
                if slot_index < len(AVAILABLE_SLOTS)
                else "No Slot Available"
            )

            slot_index += 1

            print(
                f"Scheduled: {course:<20} | "
                f"f(n): {f} | "
                f"Slot: {slot}"
            )

    end_time = time.time()

    print(f"\nNode Expansions   : {node_expansions}")
    print(f"Runtime           : {end_time - start_time:.6f} seconds")

# ---------------------------------------------------
# Main Program
# ---------------------------------------------------

print("\n========================================")
print("UNIVERSITY TIMETABLE REASONING ENGINE")
print("CO2 - SEARCH ALGORITHMS")
print("========================================")

print("\nCourses to Schedule:")
for course in COURSE_DATABASE:
    print(f"  - {course}")

print("\nAvailable Time Slots:")
for slot in AVAILABLE_SLOTS:
    print(f"  - {slot}")

# Execute All Algorithms

bfs_search()

dfs_search()

ucs_search()

greedy_search()

a_star_search()

print("\n========================================")
print("SEARCH COMPLETED")
print("========================================")
