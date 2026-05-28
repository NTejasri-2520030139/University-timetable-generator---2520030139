# ---------------------------------------------------
# CO1 - Intelligent Agent Model
# University Timetable Reasoning Engine
# ---------------------------------------------------

from dataclasses import dataclass
from typing import List, Dict

# ---------------------------------------------------
# Timetable State Representation
# ---------------------------------------------------

@dataclass
class TimetableState:
    courses: List[str]
    faculty_available: List[str]
    rooms_available: List[str]
    time_slots: List[str]

# ---------------------------------------------------
# Timetable Agent
# ---------------------------------------------------

class TimetableAgent:

    def __init__(self):

        # Knowledge Base
        # Course -> Required Resources

        self.knowledge_base: Dict[str, dict] = {

            "Mathematics": {
                "faculty": "Dr. Sharma",
                "room_type": "Lecture Hall",
                "capacity_needed": 60,
                "duration": 1
            },

            "Physics": {
                "faculty": "Dr. Rao",
                "room_type": "Lab",
                "capacity_needed": 30,
                "duration": 2
            },

            "Computer Science": {
                "faculty": "Dr. Mehta",
                "room_type": "Computer Lab",
                "capacity_needed": 40,
                "duration": 1
            },

            "Chemistry": {
                "faculty": "Dr. Nair",
                "room_type": "Lab",
                "capacity_needed": 35,
                "duration": 2
            },

            "English": {
                "faculty": "Dr. Kapoor",
                "room_type": "Classroom",
                "capacity_needed": 50,
                "duration": 1
            }
        }

        # Room Database

        self.room_database: Dict[str, dict] = {

            "Lecture Hall A": {
                "type": "Lecture Hall",
                "capacity": 80
            },

            "Lab 101": {
                "type": "Lab",
                "capacity": 40
            },

            "Computer Lab B": {
                "type": "Computer Lab",
                "capacity": 45
            },

            "Classroom 201": {
                "type": "Classroom",
                "capacity": 60
            }
        }

    # --------------------------------------------------
    # Room Suitability Check
    # --------------------------------------------------

    def is_room_suitable(self, course_name, room_name):

        course = self.knowledge_base[course_name]
        room = self.room_database[room_name]

        type_match = (
            course["room_type"] == room["type"]
        )

        capacity_match = (
            room["capacity"] >= course["capacity_needed"]
        )

        return type_match and capacity_match

    # --------------------------------------------------
    # Schedule Generation Function
    # --------------------------------------------------

    def generate_schedule(self, state: TimetableState):

        schedule = []

        print("\nGenerating Timetable...\n")

        slot_index = 0

        for course in state.courses:

            if course not in self.knowledge_base:
                print(f"Unknown Course: {course}\n")
                continue

            info = self.knowledge_base[course]

            print(f"Processing Course: {course}")
            print(f"Required Faculty  : {info['faculty']}")
            print(f"Required Room Type: {info['room_type']}")
            print(f"Capacity Needed   : {info['capacity_needed']}")

            # Check Faculty Availability

            faculty_ok = (
                info["faculty"] in state.faculty_available
            )

            print(f"Faculty Available : {faculty_ok}")

            # Find Suitable Room

            assigned_room = None

            for room in state.rooms_available:

                if self.is_room_suitable(course, room):

                    assigned_room = room
                    break

            print(f"Assigned Room     : {assigned_room}")

            # Assign Time Slot

            if (
                faculty_ok
                and assigned_room is not None
                and slot_index < len(state.time_slots)
            ):

                assigned_slot = state.time_slots[slot_index]

                slot_index += 1

                entry = {
                    "course": course,
                    "faculty": info["faculty"],
                    "room": assigned_room,
                    "time_slot": assigned_slot
                }

                schedule.append(entry)

                print(f"Scheduled At      : {assigned_slot}")
                print("Status            : SCHEDULED\n")

            else:

                print("Status            : FAILED - Resource Unavailable\n")

        return schedule

# ---------------------------------------------------
# Main Program
# ---------------------------------------------------

state = TimetableState(

    courses=[
        "Mathematics",
        "Physics",
        "Computer Science",
        "Chemistry",
        "English"
    ],

    faculty_available=[
        "Dr. Sharma",
        "Dr. Rao",
        "Dr. Mehta",
        "Dr. Nair",
        "Dr. Kapoor"
    ],

    rooms_available=[
        "Lecture Hall A",
        "Lab 101",
        "Computer Lab B",
        "Classroom 201"
    ],

    time_slots=[
        "Monday 9AM",
        "Monday 11AM",
        "Tuesday 9AM",
        "Tuesday 11AM",
        "Wednesday 9AM"
    ]
)

agent = TimetableAgent()

result = agent.generate_schedule(state)

print("------------------------------------------------")
print("FINAL TIMETABLE:")
print("------------------------------------------------")

for entry in result:

    print(
        f"Course     : {entry['course']}\n"
        f"Faculty    : {entry['faculty']}\n"
        f"Room       : {entry['room']}\n"
        f"Time Slot  : {entry['time_slot']}\n"
        f"------------------------------------------------"
    )
